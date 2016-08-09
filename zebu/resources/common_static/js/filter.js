is_all_selected();
initialize();

$("a,input,button").focus(function(){this.blur()});
function is_all_selected() {
    var select_product_count = $("button[name='filter-product'][aria-checked='true']").length;
    var select_status_count = $("button[name='filter-status'][aria-checked='true']").length;
    var select_product_sum = $("button[name='filter-product']").length;
    var select_status_sum = $("button[name='filter-status']").length;

    //Check Product
    if (select_product_count > 0) {
        if (select_product_count == select_product_sum) {
            $("button[name='filter-product']").each(function (i, o) {
                $(o).attr("aria-checked", "false");
                $(o).attr("class", "btn btn-xs btn-white");
            });
            $("#select_all_product").attr("class", "btn btn-xs btn-all");
        }
        else {
            $("#select_all_product").attr("class", "btn btn-xs btn-white");
        }
    }
    else {
        $("#select_all_product").attr("class", "btn btn-xs btn-all");
    }

    //Check Status
    if (select_status_count > 0) {
        if (select_status_count == select_status_sum) {
            $("button[name='filter-status']").each(function (i, o) {
                $(o).attr("aria-checked", "false");
                $(o).attr("class", "btn btn-xs btn-white");
            });
            $("#select_all_status").attr("class", "btn btn-xs btn-all");
        }
        else {
            $("#select_all_status").attr("class", "btn btn-xs btn-white");
        }
    }
    else {
        $("#select_all_status").attr("class", "btn btn-xs btn-all");
    }
}

function select_all(item) {
    $("button[name='filter-" + item + "']").each(function (i, o) {
        $(o).attr("aria-checked", "false");
        $(o).attr("class", "btn btn-xs btn-white");
    });
    $("#select_all_" + item).attr("class", "btn btn-xs btn-all");
}

$("button[name='filter-product']").click(function () {
    var select_filter = $("#" + this.id);
    if (select_filter.attr("aria-checked") == "false") {
        select_filter.attr("aria-checked", "true");
        select_filter.addClass("filter-selected");
    }
    else {
        select_filter.attr("aria-checked", "false");
        select_filter.removeClass("filter-selected");
    }

    is_all_selected();
    
});

$("button[name='filter-status']").click(function () {
    var select_filter = $("#" + this.id);
    if (select_filter.attr("aria-checked") == "false") {
        select_filter.attr("aria-checked", "true");
        select_filter.addClass("filter-selected");
    }
    else {
        select_filter.attr("aria-checked", "false");
        select_filter.removeClass("filter-selected");
    }

    is_all_selected();
});

function get_status()
{
    var status = [];
    $("button[name='filter-status'][aria-checked='true']").each(function (i, o) {
        status.push($(o).attr("id"));
    });
    return status;
}

function get_product()
{
    var product = [];
    $("button[name='filter-product'][aria-checked='true']").each(function (i, o) {
        product.push($(o).attr("id"));
    });
    return product;
}

function initialize()
{
    var filter = [];
    filter = $("#filter").val().substr(0,$("#filter").val().length-1).split(",");
    var filter_product = [];
    var filter_status = [];
    for (x in filter)
    {
        if (filter[x].substr(0,1) == "p")
        {
            $("#" + filter[x]).attr("aria-checked", "true");
            $("#" + filter[x]).addClass("filter-selected");
            $("#select_all_product").attr("class", "btn btn-white btn-xs");
        }
        if (filter[x].substr(0,1) == "s")
        {
            $("#" + filter[x]).attr("aria-checked", "true");
            $("#" + filter[x]).addClass("filter-selected");
            $("#select_all_status").attr("class", "btn btn-white btn-xs");
        }
    }
}
