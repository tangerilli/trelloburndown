function setup_router_handlers(router) {
    $(document).on('click', '.route_link', function() {
        var href = $(this).attr('href');
        if(href[0] == "/") {
            href = href.substr(1, href.length-1);
        }
        var success = router.navigate(href, true);
        return !success;
    });
    window.addEventListener('popstate', function(e) {
        router.navigate(location.pathname.substr(1), true);
    });
}