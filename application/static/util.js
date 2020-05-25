function submitResult(deleteData) {
  console.log(deleteData);
  if (confirm('Are you sure you wish to delete?') == false) {
    return false;
  } else {
    return true;
  }
}

// (function () {
//   alert('Script!');
// })();

document.querySelector('#deleteButton').addEventListener('onmouseover', () => {
  if (confirm('Are you sure you wish to delete?') == false) {
    return false;
  } else {
    return true;
  }
});
