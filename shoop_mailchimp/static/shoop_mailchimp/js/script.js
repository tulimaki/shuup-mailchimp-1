$(function() {
    $("form.newsletter-subscription").on("submit", function(event) {
        event.preventDefault();
        sendSubscription(this);
        return false;
    });
});
