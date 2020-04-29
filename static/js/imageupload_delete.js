function delete_image(identifier) {
    $("#image_" + identifier).addClass("hidden");
    $("#add_image_" + identifier).removeClass("hidden");
    $("#img_add_btn_" + identifier).addClass("hidden");
}

function del_img() {
    $("#image").addClass("hidden");
    $("#add_image").addClass("hidden");
    $("#img_add_btn").removeClass("hidden")
}