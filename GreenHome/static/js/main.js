

const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


  setTimeout(function () {
    $('#message').fadeOut('slow');
  },3000)


document.addEventListener('DOMContentLoaded', () => {
  const teamContainer = document.querySelector('.team-container');
  const nextBtn = document.querySelector('.nxt-btn');
  const prevBtn = document.querySelector('.pre-btn');

  if (!teamContainer) {
    console.error('Team container not found');
    return;
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      teamContainer.scrollBy({ left: teamContainer.clientWidth, behavior: 'smooth' });
    });
  } else {
    console.error('Next button not found');
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      teamContainer.scrollBy({ left: -teamContainer.clientWidth, behavior: 'smooth' });
    });
  } else {
    console.error('Previous button not found');
  }
});



// FADE IN ON SCROLL CARDS

const cards = document.querySelectorAll('.scroll-animated');

document.addEventListener('scroll', function() {
  cards.forEach((card) => {
    if (isInViewport(card)) {
      card.classList.add('scroll-animated--visible');
    }
  });
});

function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.bottom > 0 &&
    rect.top < (window.innerHeight || document.documentElement.clientHeight)
  );
}




new WOW().init();


$(document).ready(function () {
  var defaultText = 'Квартал/Район';

  // Function to update the dropdown text
  function updateDropdownText() {
      var selectedCount = $('.option-state:checked').length;
      var selectAllChecked = $('.selectall-state').is(':checked');
      
      if (selectedCount > 0) {
          $('.dropdown-text-state').text('(' + selectedCount + ') Квартали//Райони');
      } else if (selectAllChecked) {
          $('.dropdown-text-state').text(defaultText);
      } else {
          $('.dropdown-text-state').text(defaultText);
      }
  }

  // AJAX to fetch states based on selected city
  $('#city').change(function () {
      var selectedCity = $(this).val();
      var dropdownMenu = $('#state-container .dropdown-menu');
      dropdownMenu.empty();

      // Clear selected states and update the dropdown text
      $('.option-state').prop('checked', false);  // Uncheck all state checkboxes
      $('.selectall-state').prop('checked', false); // Uncheck the "select all" checkbox
      $('.dropdown-text-state').text(defaultText); // Reset dropdown text

      if (selectedCity) {
        var getStatesUrl = $('#state-container').data('get-states-url');  // Get URL from data attribute
          $.ajax({
              url: getStatesUrl,
              data: { 'city': selectedCity },
              success: function (data) {
                  dropdownMenu.append(`
                      <li>
                          <a href="#">
                              <label class="m-0 w-100">
                                  <input type="checkbox" class="selectall-state" />
                                  <span class="select-text-state">Избери всички</span>
                              </label>
                          </a>
                      </li>
                      <li class="divider"></li>
                  `);
                  $.each(data.states, function (index, state) {
                      dropdownMenu.append(`
                          <li>
                              <a href="#">
                                  <label class="m-0 w-100">
                                      <input name="state[]" type="checkbox" class="option-state" value="${state}" />
                                      ${state}
                                  </label>
                              </a>
                          </li>
                      `);
                  });
              },
              error: function () {
                  console.log('Error fetching states');
              }
          });
          $('#state-container .dropdown-toggle').prop('disabled', false);
      } else {
          $('#state-container .dropdown-toggle').prop('disabled', true);
          dropdownMenu.append('<li><a href="#"><label class="m-0 w-100">Квартал</label></a></li>');
      }
  });

  // Handle individual checkbox change for states
  $(document).on('change', '.option-state', function () {
      var totalOptions = $('.option-state').length;
      var selectedOptions = $('.option-state:checked').length;
      
      $('.selectall-state').prop('checked', totalOptions === selectedOptions);
      updateDropdownText();
  });

  // Handle select all functionality
  $(document).on('click', '.selectall-state', function () {
      var isChecked = $(this).is(':checked');
      $('.option-state').prop('checked', isChecked);
      $(".select-text-state").html(isChecked ? 'Премахни всички' : 'Избери всички');
      updateDropdownText();
  });
  
  // Ensure dropdown stays open
  $('body').on("click", ".dropdown-menu", function(e) {
      $(this).parent().is(".open") && e.stopPropagation();
  });
});

$(document).ready(function() {
  // Default texts for both dropdowns
  var defaultTextType = 'Тип имот';
  var defaultTextBuildingType = 'Тип на сградата';

  // Function to update dropdown text with the number of selected options
  function updateSelectedCount(checkboxClass, textClass, defaultText) {
      var selectedCount = $(checkboxClass + ':checked').length;
      $(textClass).html(selectedCount > 0 ? '(' + selectedCount + ') ' + defaultText : defaultText);
  }

  // Load selected checkboxes from URL parameters
  function loadSelectedCheckboxes() {
      var params = new URLSearchParams(window.location.search);
      
      // Load selections for type_choice
      var selectedTypeChoices = params.getAll('type_choice[]');
      $("input[type='checkbox'].justone").each(function() {
          $(this).prop('checked', selectedTypeChoices.includes($(this).val()));
      });
      
      // Load selections for building_type
      var selectedBuildingTypes = params.getAll('building_type[]');
      $("input[type='checkbox'].option-building-type").each(function() {
          $(this).prop('checked', selectedBuildingTypes.includes($(this).val()));
      });
      
      // Update dropdown text with selected counts
      updateSelectedCount('.justone', '.dropdown-text', defaultTextType);
      updateSelectedCount('.option-building-type', '.dropdown-text-building-type', defaultTextBuildingType);
  }

  // Handle individual checkbox change for type_choice
  $("input[type='checkbox'].justone").change(function() {
      var totalOptions = $("input[type='checkbox'].justone").length;
      var selectedOptions = $("input[type='checkbox'].justone:checked").length;

      // Check/uncheck select all box based on selections
      $('.selectall').prop('checked', totalOptions === selectedOptions);
      $(".select-text").html(selectedOptions > 0 ? 'Премахни всички' : 'Избери всички');

      updateSelectedCount('.justone', '.dropdown-text', defaultTextType);
  });

  // Handle select all/deselect all for type_choice
  $('.selectall').click(function() {
      var isChecked = $(this).is(':checked');
      $('.justone').prop('checked', isChecked);
      $(".select-text").html(isChecked ? 'Премахни всички' : 'Избери всички');
      updateSelectedCount('.justone', '.dropdown-text', defaultTextType);
  });

  // Handle individual checkbox change for building_type
  $("input[type='checkbox'].option-building-type").change(function() {
      var totalOptions = $("input[type='checkbox'].option-building-type").length;
      var selectedOptions = $("input[type='checkbox'].option-building-type:checked").length;

      // Check/uncheck select all box based on selections
      $('.selectall-building-type').prop('checked', totalOptions === selectedOptions);
      $(".select-text-building-type").html(selectedOptions > 0 ? 'Премахни всички' : 'Избери всички');

      updateSelectedCount('.option-building-type', '.dropdown-text-building-type', defaultTextBuildingType);
  });

  // Handle select all/deselect all for building_type
  $('.selectall-building-type').click(function() {
      var isChecked = $(this).is(':checked');
      $('.option-building-type').prop('checked', isChecked);
      $(".select-text-building-type").html(isChecked ? 'Премахни всички' : 'Избери всички');
      updateSelectedCount('.option-building-type', '.dropdown-text-building-type', defaultTextBuildingType);
  });

  // Ensure that clicking inside the dropdown menu doesn't close it
  $('body').on("click", ".dropdown-menu", function(e) {
      $(this).parent().is(".open") && e.stopPropagation();
  });

  // Load selected checkboxes on page load
  loadSelectedCheckboxes();
});




// INQUIRIES IMAGES UPLOADED
const imageUpload = document.getElementById('image-upload');
const uploadButton = document.getElementById('upload-button');
const imagePreview = document.getElementById('image-preview');

let images = [];

// Trigger file input when button is clicked
uploadButton.addEventListener('click', () => {
    imageUpload.click();
});

// Handle image upload
imageUpload.addEventListener('change', (event) => {
    const files = Array.from(event.target.files);

    if (images.length + files.length > 5) {
        alert('Максимум 5 снимки.');
        return;
    }

    files.forEach(file => {
        if (images.length < 5) {
            const reader = new FileReader();

            reader.onload = (e) => {
                const imageUrl = e.target.result;
                addImage(imageUrl);
            };

            reader.readAsDataURL(file);
        }
    });
});

// Add image to the preview
function addImage(url) {
    const container = document.createElement('div');
    container.classList.add('image-container');

    const img = document.createElement('img');
    img.src = url;

    const removeBtn = document.createElement('button');
    removeBtn.innerText = 'X';
    removeBtn.classList.add('remove-btn');
    removeBtn.addEventListener('click', () => removeImage(container));

    container.appendChild(img);
    container.appendChild(removeBtn);
    imagePreview.appendChild(container);

    images.push(url);
    updateImageCount();
}

// Remove image from the preview
function removeImage(container) {
    imagePreview.removeChild(container);
    images = images.filter(img => img !== container.querySelector('img').src);
    updateImageCount();
}




    // // Testimonials carousel
    // $('.testimonial-carousel').owlCarousel({
    //     autoplay: true,
    //     smartSpeed: 1000,
    //     loop: true,
    //     nav: false,
    //     dots: true,
    //     items: 1,
    //     dotsData: true,
    // });

