function local_update(url, id_to_insert_html) {
    $.get(url, function (data) {
        if (data === "reset") {
            // Display the refresh modal
            $("#refresh").modal({
                    backdrop: 'static',
                    keyboard: false
                  })
        } else {
            $(id_to_insert_html).html(data);
            setTimeout(function () {
                local_update(url, id_to_insert_html)
            }, 2000)
        }
    });

}

$(document).ready(function () {
    // If id the admin go to this page
    if (document.getElementById("admin-html-container")) {
        // If we have the table state to update
        if (document.getElementById("table-position-state")) {
            local_update("/local-update-admin", "#table-position-state")
        }
        // If is the user
    } else {
        // Table state update
        if (document.getElementById("table-position-form")) {
            local_update("/local-update", "#html-container")
            // Monopole request update the user list
        } else if (document.getElementById("monopole")) {
            local_update("/local-update", "#monopoleForm")
        }
    }
});