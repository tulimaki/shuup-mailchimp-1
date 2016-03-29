$(function() {
    $("form.newsletter-subscription").on("submit", function() {
        sendSubscription(this);
        return false;
    });
});
