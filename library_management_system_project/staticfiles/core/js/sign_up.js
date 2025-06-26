document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const courseSelect = document.getElementById("course");
  const yearSelect = document.getElementById("year");
  const yearWrapper = document.getElementById("year-wrapper");
  const finalInput = document.getElementById("final-course-input");
  const previewInput = document.getElementById("course-preview");
  const admissionYearSelect = document.getElementById("admission_year");
  const passoutYearSelect = document.getElementById("passout_year");
  const phoneInput = document.querySelector("input[name='phone_number']");

  const UG_COURSES = ["bsc", "ba", "bcom"];
  const PG_COURSES = ["msc", "ma", "mcom"];

  const romanMap = {
    "1": { roman: "I", suffix: "st" },
    "2": { roman: "II", suffix: "nd" },
    "3": { roman: "III", suffix: "rd" },
  };

  const courseLabels = {
    bsc: "B.Sc",
    ba: "B.A",
    bcom: "B.Com",
    msc: "M.Sc",
    ma: "M.A",
    mcom: "M.Com",
  };

  // Update year options when course changes
  courseSelect.addEventListener("change", () => {
    const selectedCourse = courseSelect.value;
    yearSelect.innerHTML = "";

    let options = [];
    if (UG_COURSES.includes(selectedCourse)) {
      options = ["1", "2", "3"];
    } else if (PG_COURSES.includes(selectedCourse)) {
      options = ["1", "2"];
    }

    const defaultOption = document.createElement("option");
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = "Select year";
    yearSelect.appendChild(defaultOption);

    options.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = romanMap[value].roman;
      yearSelect.appendChild(option);
    });

    yearWrapper.style.display = "block";
    finalInput.value = "";
    previewInput.value = "";
    passoutYearSelect.value = "";
  });

  // When course year changes
  yearSelect.addEventListener("change", () => {
    updateCourseLabel();
    updatePassoutYear();
  });

  // Also recalculate when admission year changes
  admissionYearSelect.addEventListener("change", () => {
    updatePassoutYear();
  });

  function updateCourseLabel() {
    const course = courseSelect.value;
    const yearValue = yearSelect.value;
    if (!course || !yearValue) return;

    const { roman, suffix } = romanMap[yearValue];
    const fullCourse = `${roman}${suffix} ${courseLabels[course]}`;
    finalInput.value = fullCourse;
    previewInput.value = fullCourse;
  }

//   calculating passout year

  function updatePassoutYear() {
  const course = courseSelect.value.toLowerCase();
  const admissionYear = parseInt(admissionYearSelect.value);

  const courseDurations = {
    bsc: 3,
    ba: 3,
    bcom: 3,
    msc: 2,
    ma: 2,
    mcom: 2,
  };

  if (!isNaN(admissionYear) && course in courseDurations) {
    const passoutYear = admissionYear + courseDurations[course];
    passoutYearSelect.value = passoutYear.toString();
  } else {
    passoutYearSelect.value = "";
  }
}
function showToast(message) {
  const toastMessage = document.getElementById("toast-message");
  toastMessage.textContent = message;

  const toast = new bootstrap.Toast(document.getElementById("formToast"));
  toast.show();
}


  form.addEventListener("submit", function (e) {
  const phone = phoneInput.value.trim();
  const isValidPhone = /^\d{10}$/.test(phone);
  if (!isValidPhone) {
    e.preventDefault();
    showToast("Please enter a valid 10-digit phone number.");
    phoneInput.classList.add("is-invalid");
    phoneInput.focus();
    return;
  } else {
    phoneInput.classList.remove("is-invalid");
  }

  const admissionYear = parseInt(admissionYearSelect.value);
  const passoutYear = parseInt(passoutYearSelect.value);
  const currentYear = new Date().getFullYear();

  if (admissionYear > currentYear) {
    e.preventDefault();
    showToast("Admission year cannot be in the future.");
    admissionYearSelect.classList.add("is-invalid");
    return;
  }

  if (admissionYear >= passoutYear) {
    e.preventDefault();
    showToast("Admission year must be less than Passout year.");
    admissionYearSelect.classList.add("is-invalid");
    passoutYearSelect.classList.add("is-invalid");
    return;
  }

  if (passoutYear < currentYear) {
    e.preventDefault();
    showToast("You cannot register because your passout year has already passed.");
    passoutYearSelect.classList.add("is-invalid");
    return;
  }

  // If everything is valid
  admissionYearSelect.classList.remove("is-invalid");
  passoutYearSelect.classList.remove("is-invalid");
});

});