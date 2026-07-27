# GreenHome: преминаване от S3 presigned URL-и към CloudFront кеширане

## 1. Цел и текущо състояние

Целта е публичните снимки на имотите и статичните файлове на GreenHome да се зареждат през Amazon CloudFront, а S3 bucket-ът да остане private. Така:

- URL адресите няма да се променят при всяко зареждане;
- браузърът и CloudFront ще могат да кешират файловете;
- S3 ще обслужва основно първото зареждане на даден файл във всяка CloudFront edge локация;
- директният публичен достъп до S3 ще остане забранен;
- снимките, изпратени от клиенти чрез формата за запитване, ще останат частни.

Проверено състояние към 27.07.2026 г.:

- production сайтът генерира S3 presigned URL-и с `X-Amz-*` параметри и срок 3600 секунди;
- неподписан директен URL към съществуваща S3 снимка връща `403 Forbidden`, тоест bucket-ът действително не е публичен;
- локалният `GreenHome/settings.py` вече съдържа `AWS_QUERYSTRING_AUTH = False` и `CacheControl`, но все още няма CloudFront custom domain;
- не трябва да се deploy-ва само `AWS_QUERYSTRING_AUTH = False`, защото private S3 bucket-ът няма да приеме неподписаните директни URL-и;
- `listings.Photos` и `realtors.Realtor.photo` са публични файлове под `photos/`;
- `inquiry_message.ImagesInquiry.image` е под `inquiries/images/` и трябва да остане private.

Препоръчителната архитектура е:

```text
Посетител -> CloudFront -> OAC -> private S3
                  |
                  +-- /photos/*       публични снимки на имоти и брокери
                  +-- /static/*       публични CSS, JS, изображения и шрифтове

Django admin -> presigned S3 URL -> /inquiries/images/*
                                  частни клиентски файлове
```

## 2. Важни правила преди започване

1. Не правете S3 bucket-а public.
2. Не изключвайте **Block all public access**.
3. Използвайте **Origin Access Control (OAC)**, а не стария **Origin Access Identity (OAI)**.
4. Не deploy-вайте промяната в Django, преди CloudFront URL-ът да е тестван успешно.
5. Не давайте на CloudFront достъп до `inquiries/images/*`.
6. Направете промените първо с CloudFront домейна `dXXXXXXXXXXXX.cloudfront.net`. Собствен CDN поддомейн може да се добави по-късно.
7. Запишете текущия работещ Render commit, за да може лесно да се направи rollback.

## 3. Измерване преди промяната

Това дава база за сравнение на разходите преди и след CloudFront.

### 3.1. Размер и брой на файловете

От AWS Console:

1. Отворете **Amazon S3**.
2. В лявото меню изберете **Storage Lens** -> **Dashboards**.
3. Отворете `default-account-dashboard`.
4. Филтрирайте по bucket `greenhomebucket1`.
5. Запишете стойностите за **Total storage** и **Object count**.

Безплатните Storage Lens метрики са дневни и са достатъчни за общия размер на bucket-а. Prefix-level activity метриките са платена Advanced функция и не е необходимо да се включват само за тази миграция.

Ако има конфигуриран AWS CLI, размерът само на публичните снимки може да се провери с:

```powershell
aws s3 ls s3://greenhomebucket1/photos/ --recursive --summarize --human-readable
```

### 3.2. Текущи разходи

1. Отворете **Billing and Cost Management**.
2. Изберете **Cost Explorer** -> **Cost and usage**.
3. Задайте период поне последните 3 месеца.
4. При **Group by** изберете **Service**.
5. Филтрирайте по **Amazon Simple Storage Service**.
6. Запишете месечните стойности.
7. При нужда групирайте и по **Usage type**, за да се видят request и data-transfer разходите.

## 4. Създаване на CloudFront distribution с OAC

AWS периодично променя вида на конзолата. Следните имена са по актуалния CloudFront wizard; при малки визуални разлики търсете същите полета.

1. Влезте в [AWS CloudFront Console](https://console.aws.amazon.com/cloudfront/v4/home).
2. Изберете **Create distribution**.
3. В **Distribution name** въведете например `greenhome-public-assets`.
4. Изберете **Single website or app** -> **Next**.
5. При **Origin type** изберете **Amazon S3**.
6. При **S3 origin** натиснете **Browse S3** и изберете `greenhomebucket1`.
7. Изберете нормалния S3 bucket endpoint, а не **S3 website endpoint**. OAC не работи със website endpoint.
8. При **Settings** изберете **Use recommended origin settings**. Това създава OAC и избира подписване на origin заявките.
9. Ако конзолата покаже подробните OAC настройки, проверете:
   - **Origin access**: `Origin access control settings (recommended)`;
   - **Signing behavior**: `Sign requests (recommended)`;
   - **Origin access control**: създаден или избран OAC за този bucket.
10. Натиснете **Next**.
11. При **Enable security protections** не е необходимо да включвате AWS WAF само за изображения и static assets. WAF може да се добави по-късно и има отделна цена.
12. Не добавяйте собствен domain на този етап.
13. Прегледайте настройките и изберете **Create distribution**.
14. CloudFront трябва автоматично да предложи/направи промяна в S3 bucket policy. Позволете автоматичното update-ване, ако wizard-ът го поиска.
15. Изчакайте статусът да спре да бъде **Deploying**.
16. Запишете:
   - **Distribution ID**;
   - **Distribution domain name**, например `d123example.cloudfront.net`.

## 5. Ограничаване на CloudFront само до публичните prefixes

Автоматично генерираната policy често позволява на distribution-а `s3:GetObject` върху целия bucket. За този проект това не е желателно, защото bucket-ът съдържа и `inquiries/images/`.

### 5.1. Проверка на S3 Block Public Access

1. Отворете **Amazon S3** -> **General purpose buckets**.
2. Изберете `greenhomebucket1`.
3. Отворете таб **Permissions**.
4. При **Block public access (bucket settings)** проверете, че **Block all public access** е `On`.
5. Не изключвайте тази настройка. OAC работи с private bucket.

### 5.2. Ограничаване на bucket policy

1. В същия таб **Permissions** намерете **Bucket policy**.
2. Изберете **Edit**.
3. Намерете statement-а, чийто principal е:

```json
{"Service": "cloudfront.amazonaws.com"}
```

4. Проверете, че condition-ът съдържа точния CloudFront distribution ARN:

```json
"Condition": {
  "StringEquals": {
    "AWS:SourceArn": "arn:aws:cloudfront::<AWS_ACCOUNT_ID>:distribution/<DISTRIBUTION_ID>"
  }
}
```

5. Ограничете `Resource` само до публичните пътища:

```json
{
  "Sid": "AllowCloudFrontReadOnlyPublicAssets",
  "Effect": "Allow",
  "Principal": {
    "Service": "cloudfront.amazonaws.com"
  },
  "Action": "s3:GetObject",
  "Resource": [
    "arn:aws:s3:::greenhomebucket1/photos/*",
    "arn:aws:s3:::greenhomebucket1/static/*"
  ],
  "Condition": {
    "StringEquals": {
      "AWS:SourceArn": "arn:aws:cloudfront::<AWS_ACCOUNT_ID>:distribution/<DISTRIBUTION_ID>"
    }
  }
}
```

6. Заменете `<AWS_ACCOUNT_ID>` и `<DISTRIBUTION_ID>` с реалните стойности.
7. Не изтривайте други statements, нужни на Render/Django за upload и администриране на файловете.
8. Изберете **Save changes**.

Важно: не добавяйте `inquiries/images/*` в CloudFront statement-а.

## 6. Настройване на CloudFront cache behavior

1. Отворете **CloudFront** -> **Distributions**.
2. Изберете създадения distribution.
3. Отворете таб **Behaviors**.
4. Маркирайте default behavior-а `Default (*)` и изберете **Edit**.
5. Задайте:
   - **Viewer protocol policy**: `Redirect HTTP to HTTPS`;
   - **Allowed HTTP methods**: `GET, HEAD`;
   - **Cache policy**: `CachingOptimized`;
   - **Origin request policy**: празна/`None`, освен ако wizard-ът не изисква managed S3 policy;
   - **Compress objects automatically**: `Yes`, ако полето е налично.
6. Изберете **Save changes**.

Managed policy `CachingOptimized`:

- не включва query strings в cache key;
- не включва cookies;
- кешира до 365 дни;
- поддържа Gzip/Brotli cache variants чрез нормализиран `Accept-Encoding`.

Тъй като публичните URL-и вече няма да имат `X-Amz-*` query параметри, един и същ файл ще има постоянен CloudFront URL.

## 7. Първи тест на CloudFront преди промяна в Django

Вземете съществуващ публичен S3 key, например:

```text
photos/example.jpg
```

Отворете:

```text
https://dXXXXXXXXXXXX.cloudfront.net/photos/example.jpg
```

Очакван резултат: снимката се отваря с HTTP `200`.

След това проверете несъществуващ или тестов private път:

```text
https://dXXXXXXXXXXXX.cloudfront.net/inquiries/images/private-test.jpg
```

Очакван резултат: HTTP `403` или `404`, но не и съдържание на private файл.

Директният неподписан S3 адрес също трябва да остане забранен:

```text
https://greenhomebucket1.s3.amazonaws.com/photos/example.jpg
```

Очакван резултат: `403 Forbidden`.

Не продължавайте към production deploy, ако CloudFront URL-ът не връща публичната снимка или ако CloudFront може да прочете `inquiries/images/*`.

## 8. Отделяне на private inquiry storage в Django

Това трябва да бъде направено, защото `AWS_QUERYSTRING_AUTH = False` и CloudFront са подходящи за публичните имотни снимки, но не и за изпратени от клиентите файлове.

### 8.1. Нов файл `GreenHome/storage_backends.py`

Създайте:

```python
from storages.backends.s3 import S3Storage


class PrivateInquiryStorage(S3Storage):
    """Private S3 storage with short-lived presigned URLs."""

    def __init__(self, **options):
        options.setdefault("custom_domain", None)
        options.setdefault("querystring_auth", True)
        options.setdefault("querystring_expire", 3600)
        options.setdefault("default_acl", None)
        options.setdefault("file_overwrite", False)
        options.setdefault(
            "object_parameters",
            {"CacheControl": "private, no-store"},
        )
        super().__init__(**options)
```

### 8.2. Промяна в `inquiry_message/models.py`

Добавете import:

```python
from GreenHome.storage_backends import PrivateInquiryStorage
```

Създайте storage instance:

```python
private_inquiry_storage = PrivateInquiryStorage()
```

Променете само полето за inquiry изображения:

```python
image = models.ImageField(
    upload_to="inquiries/images/",
    storage=private_inquiry_storage,
    blank=True,
    null=True,
)
```

Това не променя съхранения key в базата. Съществуващите `inquiries/images/...` файлове остават на същото място, но техните `.url` адреси продължават да бъдат подписани S3 URL-и.

### 8.3. Migration и проверки

Изпълнете локално:

```powershell
python manage.py makemigrations inquiry_message
python manage.py check
python manage.py test
```

Прегледайте генерираната migration преди commit. Тя трябва да променя само storage конфигурацията на полето, без да мести или изтрива файлове.

## 9. Django 5 и django-storages конфигурация

Проектът използва Django 5.0.7 и django-storages 1.14.4. За Django 5 използвайте `STORAGES`, вместо старите `DEFAULT_FILE_STORAGE` и `STATICFILES_STORAGE`.

В `GreenHome/settings.py` запазете AWS credentials и region от environment variables, но заменете production static/media частта с конфигурация по този модел:

```python
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_VERIFY = True
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

if not DEBUG:
    if not AWS_S3_CUSTOM_DOMAIN:
        raise RuntimeError("AWS_S3_CUSTOM_DOMAIN is required in production")

    public_cache_parameters = {
        "CacheControl": "public, max-age=31536000, immutable",
    }

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "region_name": AWS_S3_REGION_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "querystring_auth": False,
                "file_overwrite": False,
                "default_acl": None,
                "object_parameters": public_cache_parameters,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3ManifestStaticStorage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "region_name": AWS_S3_REGION_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "querystring_auth": False,
                "location": "static",
                "default_acl": None,
                "object_parameters": public_cache_parameters,
            },
        },
    }

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

След тази промяна премахнете дублиращите production настройки:

```python
DEFAULT_FILE_STORAGE = ...
STATICFILES_STORAGE = ...
AWS_QUERYSTRING_AUTH = ...
AWS_S3_OBJECT_PARAMETERS = ...
```

Причината `AWS_QUERYSTRING_AUTH = False` да не е глобална настройка в предложения вариант е, че public и private storage-ите имат различни изисквания.

`S3ManifestStaticStorage` добавя content hash към имената на static файловете. Това прави `immutable` безопасно: при промяна на CSS/JS се създава нов URL, вместо да се презаписва дълго кешираният стар URL.

## 10. Локална проверка на генерираните URL-и

С production-like environment variables, но с тестова конфигурация, проверете:

```powershell
python manage.py shell
```

В Django shell:

```python
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from GreenHome.storage_backends import PrivateInquiryStorage

print(default_storage.url("photos/test.jpg"))
print(staticfiles_storage.url("css/style.css"))
print(PrivateInquiryStorage().url("inquiries/images/test.jpg"))
```

Очаквания:

- public media URL започва с `https://dXXXXXXXXXXXX.cloudfront.net/photos/`;
- static URL започва с `https://dXXXXXXXXXXXX.cloudfront.net/static/`;
- public URL-ите нямат `X-Amz-*`;
- private inquiry URL сочи към S3 и съдържа `X-Amz-*`.

Изпълнете и:

```powershell
python manage.py collectstatic --noinput
python manage.py check
python manage.py test
```

Ако `collectstatic` съобщи липсващ файл, не изключвайте manifest storage на сляпо. Поправете липсващия `{% static %}`/CSS asset reference и изпълнете командата отново.

## 11. Обновяване на Cache-Control за съществуващите снимки

`object_parameters` се прилага при нов upload. То не променя автоматично metadata на вече съществуващите `photos/*` обекти.

Първо тествайте с една снимка:

1. Отворете **Amazon S3** -> **General purpose buckets** -> `greenhomebucket1`.
2. Отворете prefix/folder `photos/`.
3. Маркирайте една тестова снимка.
4. От **Actions** изберете **Copy**.
5. При destination изберете чрез **Browse S3** същия bucket и същия път.
6. При **Additional copy settings** изберете **Specify settings**.
7. В секция **Metadata** изберете **Replace all metadata**.
8. Изберете **Add metadata**.
9. При **Type** изберете `System-defined`.
10. При key изберете/въведете `Cache-Control`.
11. При value въведете:

```text
public, max-age=31536000, immutable
```

12. Запазете оригиналния `Content-Type` (`image/jpeg`, `image/png`, `image/webp` и т.н.). При **Replace all metadata** трябва да бъдат запазени всички други metadata стойности, които са нужни.
13. Изберете **Copy**.
14. Проверете от таб **Properties** на обекта, че `Cache-Control` и `Content-Type` са правилни.
15. Проверете снимката през CloudFront.

След успешен тест повторете операцията batch-ово за `photos/`. AWS предупреждава да се изчака Copy операцията да завърши, преди в обработвания folder да се качват нови обекти. Ако броят е голям, използвайте AWS CLI/SDK или S3 Batch Operations вместо ръчно избиране на хиляди файлове.

Не задавайте public cache metadata върху `inquiries/images/*`.

## 12. Настройка в Render

### 12.1. Environment variable

1. Отворете **Render Dashboard**.
2. Изберете GreenHome web service-а.
3. В лявото меню изберете **Environment**.
4. В **Environment Variables** изберете **+ Add Environment Variable**.
5. Добавете:

```text
Key:   AWS_S3_CUSTOM_DOMAIN
Value: dXXXXXXXXXXXX.cloudfront.net
```

Стойността е без `https://` и без `/` накрая.

6. Проверете и съществуващите variables:
   - `DEBUG=False`;
   - `AWS_STORAGE_BUCKET_NAME=greenhomebucket1`;
   - `AWS_S3_REGION_NAME=eu-central-1`;
   - AWS credentials са налични и не са записани в Git.
7. Изберете **Save only**, докато новият код още не е push-нат.

### 12.2. Build command

1. В Render service-а отворете **Settings**.
2. Намерете секция **Build & Deploy**.
3. Проверете **Build Command**.
4. Запазете текущата install команда и се уверете, че build процесът изпълнява:

```text
python manage.py collectstatic --noinput
```

Пример, само ако съответства на текущия build:

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Не заменяйте други необходими build стъпки без да ги добавите към командата.

### 12.3. Deploy на правилния commit

1. Commit-нете и push-нете Django промените и migration-а.
2. В Render service-а отворете **Events**.
3. Изберете **Manual Deploy** -> **Deploy latest commit**.
4. За първото пускане може да използвате **Clear build cache & deploy**, за да няма стари static build artifacts.
5. Проверете в deploy log:
   - правилния Git commit SHA;
   - успешен `collectstatic`;
   - успешни migrations, ако deployment процесът ги изпълнява;
   - липса на `RuntimeError: AWS_S3_CUSTOM_DOMAIN is required in production`.

Не използвайте само **Restart service**: според Render това стартира същия commit и не е начин да се качи новият код.

## 13. Проверка след production deploy

### 13.1. HTML и URL адреси

1. Отворете `https://www.greenhomebg.com` в private/incognito прозорец.
2. Отворете Browser DevTools -> **Network**.
3. Филтрирайте по `Img`, после по `CSS` и `JS`.
4. Проверете, че адресите започват с CloudFront domain-а.
5. Проверете, че никой public asset URL не съдържа:

```text
X-Amz-Algorithm
X-Amz-Credential
X-Amz-Date
X-Amz-Expires
X-Amz-Signature
```

### 13.2. Cache hit

Отворете една и съща снимка два пъти и проверете response headers. Очакват се:

```text
cache-control: public, max-age=31536000, immutable
x-cache: Hit from cloudfront
age: <число>
```

Първата заявка може да бъде `Miss from cloudfront`. Следваща заявка към същата edge локация трябва да стане `Hit from cloudfront`, освен ако браузърът вече я обслужва директно от своя cache.

### 13.3. Функционални тестове

Проверете поне:

1. началната страница;
2. списъка с обяви;
3. search резултатите;
4. детайлна страница и lightbox на имот;
5. страниците с брокери;
6. Django admin thumbnails;
7. upload на нова снимка към обява;
8. upload на тестова inquiry снимка;
9. отваряне на inquiry снимката само чрез краткотраен presigned S3 URL;
10. директният неподписан S3 URL остава `403`.

След теста изтрийте тестовото клиентско запитване/файл по нормалния административен процес, ако съдържа тестови лични данни.

## 14. CloudFront invalidation при необходимост

При content-hashed static filenames обичайно не е нужна invalidation. За файл, който е останал със същия key, може да се направи ръчно:

1. Отворете **CloudFront** -> **Distributions**.
2. Изберете distribution-а.
3. Отворете таб **Invalidations**.
4. Изберете **Create invalidation**.
5. Въведете по един path на ред, например:

```text
/photos/example.jpg
/static/css/style.abc123.css
```

6. Изберете **Create invalidation**.

Използвайте `/*` само при реална необходимост. Invalidations не могат да бъдат отменени и над безплатната квота се таксуват.

## 15. Наблюдение след промяната

### 15.1. CloudFront cache статистика

1. Отворете **CloudFront Console**.
2. В лявото меню отворете **Reports & analytics** -> **Cache statistics**.
3. Изберете distribution-а и период.
4. Следете:
   - **Hit** спрямо **Miss**;
   - bytes served to viewers;
   - bytes from misses;
   - 4xx/5xx errors.

Cache hit ratio трябва постепенно да се увеличи. В първите часове/дни е нормално да има повече misses, докато edge caches се затоплят.

### 15.2. AWS разходи

Следете поне един пълен billing месец:

1. **Billing and Cost Management** -> **Cost Explorer**.
2. Сравнете **Amazon Simple Storage Service** преди и след промяната.
3. Добавете **Amazon CloudFront** към сравнението.
4. Гледайте общата сума, не само намалението на S3 — CloudFront също струва пари.

По желание може да се ограничи CloudFront price class до Европа и Северна Америка, ако аудиторията е почти изцяло в България. Това трябва да се реши след преглед на трафика и актуалните AWS цени, а не на сляпо.

## 16. Rollback план

Ако след deploy снимките не се зареждат:

1. В Render отворете service-а -> **Events**.
2. Изберете последния известен работещ deploy/commit и използвайте rollback или deploy на конкретния стар commit.
3. Старият код ще продължи да генерира presigned S3 URL-и.
4. CloudFront distribution-ът може да остане създаден, докато проблемът се анализира.
5. Не правете bucket-а public като временна поправка.
6. Проверете последователно:
   - CloudFront distribution status;
   - OAC signing behavior;
   - S3 bucket policy и `AWS:SourceArn`;
   - разрешените `photos/*` и `static/*` resources;
   - Render `AWS_S3_CUSTOM_DOMAIN`;
   - реално deploy-натия Git commit;
   - `collectstatic` log-а.

## 17. Критерии за завършена задача

Задачата е завършена само ако всички точки са изпълнени:

- [ ] S3 **Block all public access** остава включено.
- [ ] CloudFront използва OAC и **Sign requests (recommended)**.
- [ ] CloudFront има достъп до `photos/*` и `static/*`.
- [ ] CloudFront няма достъп до `inquiries/images/*`.
- [ ] Public URLs са постоянни CloudFront URLs без `X-Amz-*`.
- [ ] Private inquiry URLs остават краткотрайни presigned S3 URLs.
- [ ] Новите public файлове получават правилен `Cache-Control`.
- [ ] Съществуващите `photos/*` metadata са обновени и проверени.
- [ ] Static файловете използват hashed filenames.
- [ ] `collectstatic`, `check` и тестовете минават успешно.
- [ ] Production страниците и admin upload-ите са проверени.
- [ ] Втората CloudFront заявка показва cache hit.
- [ ] Има записана baseline стойност и се следят общите S3 + CloudFront разходи.

## 18. Официални източници

- [AWS: Get started with a CloudFront standard distribution and OAC](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html)
- [AWS: Restrict access to an Amazon S3 origin with OAC](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- [AWS: Managed cache policy CachingOptimized](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html)
- [AWS: Require HTTPS between viewers and CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-viewers-to-cloudfront.html)
- [AWS: Block public access for S3 buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/configuring-block-public-access-bucket.html)
- [AWS: Edit existing S3 object metadata](https://docs.aws.amazon.com/AmazonS3/latest/userguide/add-object-metadata.html)
- [AWS: Create CloudFront invalidations](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation_Requests.html)
- [AWS: View CloudFront cache statistics](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-statistics.html)
- [AWS: S3 Storage Lens metrics](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_view_metrics.html)
- [django-storages: Amazon S3 backend settings](https://django-storages.readthedocs.io/en/stable/backends/amazon-S3.html)
- [Django: STORAGES setting](https://docs.djangoproject.com/en/5.0/ref/settings/#storages)
- [Django: Deploying static files and CDN storage](https://docs.djangoproject.com/en/5.0/howto/static-files/deployment/)
- [Render: Environment variables](https://render.com/docs/configure-environment-variables)
- [Render: Manual deploys and deploy options](https://render.com/docs/deploys)
