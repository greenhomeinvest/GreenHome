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



// DROPDOWN MENU FOR TYPE-CHOICES BUILDING MULTISELECTION 
$(document).ready(function() {

  var defaultText = 'Тип имот';

  // Function to update the dropdown text with the number of selected options
  function updateSelectedCount(checkboxClass, textClass, selectAllClass) {
    var selectedCount = $(checkboxClass + ':checked').length;
    var isSelectAllChecked = $(selectAllClass).is(':checked');
    if (selectedCount > 0) {
      $(textClass).html('(' + selectedCount + ') Тип имот');
  } else if (isSelectAllChecked) {
      $(textClass).html(defaultText);
  } else {
      $(textClass).html(defaultText);
  }
  }

  // Load selected checkboxes from URL parameters
  function loadSelectedCheckboxes() {
      var params = new URLSearchParams(window.location.search);
      var selectedChoices = params.getAll('type_choice[]');
      
      // Set checkboxes based on URL parameters
      $("input[type='checkbox'].justone").each(function() {
          if (selectedChoices.includes($(this).val())) {
              $(this).prop('checked', true);
          } else {
              $(this).prop('checked', false);
          }
      });

      // Update the dropdown text with the count of selected options
      updateSelectedCount('.justone', '.dropdown-text');
  }

  // Handle individual checkbox change
  $("input[type='checkbox'].justone").change(function() {
      var totalOptions = $("input[type='checkbox'].justone").length;
      var selectedOptions = $("input[type='checkbox'].justone:checked").length;

      // Check or uncheck the select all box based on individual selections
      if (totalOptions === selectedOptions) {
          $('.selectall').prop('checked', true);
          $(".select-text").html('Премахни всички');
      } else {
          $('.selectall').prop('checked', false);
          $(".select-text").html('Избери всички');
      }
      
      // Update the dropdown text with the count of selected options
      updateSelectedCount('.justone', '.dropdown-text');
  });

  // Handle select all/deselect all functionality
  $('.selectall').click(function() {
      if ($(this).is(':checked')) {
          $('.justone').prop('checked', true);
          $(".select-text").html('Премахни всички');
      } else {
          $('.justone').prop('checked', false);
          $(".select-text").html('Избери всички');
          // $(textClass).html(defaultText);
      }

      // Update the dropdown text with the count of selected options
      updateSelectedCount('.justone', '.dropdown-text');
  });

  // Ensure that clicking inside the dropdown menu doesn't close it
  $('body').on("click", ".dropdown-menu", function(e) {
      $(this).parent().is(".open") && e.stopPropagation();
  });

  // Load selected checkboxes on page load
  loadSelectedCheckboxes();
});

// DROPDOWN MENU WITH MULTISELEC FOR STATE-CHOICES 
$(document).ready(function() {
  // Default text for the dropdown button
  var defaultText = 'Квартал';

  // Function to update the dropdown text with the number of selected options
  function updateSelectedCount(checkboxClass, textClass, selectAllClass) {
      var selectedCount = $(checkboxClass + ':checked').length;
      var isSelectAllChecked = $(selectAllClass).is(':checked');
      
      if (selectedCount > 0) {
          $(textClass).html('(' + selectedCount + ') Квартали');
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
