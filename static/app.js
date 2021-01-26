function readURL(input) {
  console.log("changed")

  if (input.files && input.files[0]) {
    console.log("file is there")
      var reader = new FileReader();
      reader.onload = function(e) {
        console.log('this is too')
          $('#imagePreview').css('background-image', 'url('+e.target.result +')');
          $('#imagePreview').hide();
          $('#imagePreview').fadeIn(650);
      }
      reader.readAsDataURL(input.files[0]);
  }
}

$("document").ready(function(){
  $("#imageUpload").change(function() {
    console.log("changed")
    readURL(this);
  });
  
});

