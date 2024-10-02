

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



// // DROPDOWN MENU FOR TYPE-CHOICES BUILDING MULTISELECTION 
// $(document).ready(function() {

//   var defaultText = 'Тип имот';

//   // Function to update the dropdown text with the number of selected options
//   function updateSelectedCount(checkboxClass, textClass, selectAllClass) {
//     var selectedCount = $(checkboxClass + ':checked').length;
//     var isSelectAllChecked = $(selectAllClass).is(':checked');
//     if (selectedCount > 0) {
//       $(textClass).html('(' + selectedCount + ') Тип имот');
//   } else if (isSelectAllChecked) {
//       $(textClass).html(defaultText);
//   } else {
//       $(textClass).html(defaultText);
//   }
//   }

//   // Load selected checkboxes from URL parameters
//   function loadSelectedCheckboxes() {
//       var params = new URLSearchParams(window.location.search);
//       var selectedChoices = params.getAll('type_choice[]');
      
//       // Set checkboxes based on URL parameters
//       $("input[type='checkbox'].justone").each(function() {
//           if (selectedChoices.includes($(this).val())) {
//               $(this).prop('checked', true);
//           } else {
//               $(this).prop('checked', false);
//           }
//       });

//       // Update the dropdown text with the count of selected options
//       updateSelectedCount('.justone', '.dropdown-text');
//   }

//   // Handle individual checkbox change
//   $("input[type='checkbox'].justone").change(function() {
//       var totalOptions = $("input[type='checkbox'].justone").length;
//       var selectedOptions = $("input[type='checkbox'].justone:checked").length;

//       // Check or uncheck the select all box based on individual selections
//       if (totalOptions === selectedOptions) {
//           $('.selectall').prop('checked', true);
//           $(".select-text").html('Премахни всички');
//       } else {
//           $('.selectall').prop('checked', false);
//           $(".select-text").html('Избери всички');
//       }
      
//       // Update the dropdown text with the count of selected options
//       updateSelectedCount('.justone', '.dropdown-text');
//   });

//   // Handle select all/deselect all functionality
//   $('.selectall').click(function() {
//       if ($(this).is(':checked')) {
//           $('.justone').prop('checked', true);
//           $(".select-text").html('Премахни всички');
//       } else {
//           $('.justone').prop('checked', false);
//           $(".select-text").html('Избери всички');
//           // $(textClass).html(defaultText);
//       }

//       // Update the dropdown text with the count of selected options
//       updateSelectedCount('.justone', '.dropdown-text');
//   });

//   // Ensure that clicking inside the dropdown menu doesn't close it
//   $('body').on("click", ".dropdown-menu", function(e) {
//       $(this).parent().is(".open") && e.stopPropagation();
//   });

//   // Load selected checkboxes on page load
//   loadSelectedCheckboxes();
// });

new WOW().init();

// DROPDOWN MENU WITH MULTISELEC FOR STATE-CHOICES 
$(document).ready(function() {
  // Default text for the dropdown button
  var defaultText = 'Квартал/Район';

  // Function to update the dropdown text with the number of selected options
  function updateSelectedCount(checkboxClass, textClass, selectAllClass) {
      var selectedCount = $(checkboxClass + ':checked').length;
      var isSelectAllChecked = $(selectAllClass).is(':checked');
      
      if (selectedCount > 0) {
          $(textClass).html('(' + selectedCount + ') Квартали//Райони');
      } else if (isSelectAllChecked) {
          $(textClass).html(defaultText);
      } else {
          $(textClass).html(defaultText);
      }
  }

  // Handle individual checkbox change for states
  $("input[type='checkbox'].option-state").change(function() {
      var totalOptions = $("input[type='checkbox'].option-state").length;
      var selectedOptions = $("input[type='checkbox'].option-state:checked").length;

      // Check or uncheck the select all box based on individual selections
      if (totalOptions === selectedOptions) {
          $('.selectall-state').prop('checked', true);
          $(".select-text-state").html('Премахни всички');
      } else {
          $('.selectall-state').prop('checked', false);
          $(".select-text-state").html('Избери всички');
      }
      
      // Update the dropdown text with the count of selected options
      updateSelectedCount('.option-state', '.dropdown-text-state', '.selectall-state');
  });

  // Handle select all/deselect all functionality for states
  $('.selectall-state').click(function() {
      if ($(this).is(':checked')) {
          $('.option-state').prop('checked', true);
          $(".select-text-state").html('Премахни всички');
      } else {
          $('.option-state').prop('checked', false);
          $(".select-text-state").html('Избери всички');
      }

      // Update the dropdown text with the count of selected options
      updateSelectedCount('.option-state', '.dropdown-text-state', '.selectall-state');
  });

  // Ensure that clicking inside the dropdown menu doesn't close it
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


// // DROPDOWN MENU WITH MULTISELEC FOR STATE-CHOICES 
// $(document).ready(function() {
//   // Default text for the dropdown button
//   var defaultText = 'Тип на сградата';

//   // Function to update the dropdown text with the number of selected options
//   function updateSelectedCount(checkboxClass, textClass, selectAllClass) {
//       var selectedCount = $(checkboxClass + ':checked').length;
//       var isSelectAllChecked = $(selectAllClass).is(':checked');
      
//       if (selectedCount > 0) {
//           $(textClass).html('(' + selectedCount + ') Тип на сградата');
//       } else if (isSelectAllChecked) {
//           $(textClass).html(defaultText);
//       } else {
//           $(textClass).html(defaultText);
//       }
//   }

//   // Load selected checkboxes from URL parameters
//   function loadSelectedCheckboxes() {
//     var params = new URLSearchParams(window.location.search);
//     var selectedChoices = params.getAll('building_type[]');
    
//     // Set checkboxes based on URL parameters
//     $("input[type='checkbox'].justone").each(function() {
//         if (selectedChoices.includes($(this).val())) {
//             $(this).prop('checked', true);
//         } else {
//             $(this).prop('checked', false);
//         }
//     });

//     // Update the dropdown text with the count of selected options
//     updateSelectedCount('.justone', '.dropdown-text');
// }
// // Handle individual checkbox change
// $("input[type='checkbox'].justone").change(function() {
//   var totalOptions = $("input[type='checkbox'].justone").length;
//   var selectedOptions = $("input[type='checkbox'].justone:checked").length;

//   // Check or uncheck the select all box based on individual selections
//   if (totalOptions === selectedOptions) {
//       $('.selectall').prop('checked', true);
//       $(".select-text").html('Премахни всички');
//   } else {
//       $('.selectall').prop('checked', false);
//       $(".select-text").html('Избери всички');
//   }
  
//   // Update the dropdown text with the count of selected options
//   updateSelectedCount('.justone', '.dropdown-text');
// });

//   // Handle select all/deselect all functionality
//   $('.selectall').click(function() {
//     if ($(this).is(':checked')) {
//         $('.justone').prop('checked', true);
//         $(".select-text").html('Премахни всички');
//     } else {
//         $('.justone').prop('checked', false);
//         $(".select-text").html('Избери всички');
//         // $(textClass).html(defaultText);
//     }

//     // Update the dropdown text with the count of selected options
//     updateSelectedCount('.justone', '.dropdown-text');
// });


//  // Ensure that clicking inside the dropdown menu doesn't close it
//  $('body').on("click", ".dropdown-menu", function(e) {
//   $(this).parent().is(".open") && e.stopPropagation();
// });

// // Load selected checkboxes on page load
// loadSelectedCheckboxes();
// });



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