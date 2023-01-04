// main.js

// Initialize variables
var page = 1;
var loading = false;

// Function to get tweets from API and append them to timeline
function getTweets() {
  // Return if already loading
  if (loading) {
    return;
  }

  // Set loading to true to prevent duplicate requests
  loading = true;

  // Show loading indicator
  $('#loading').show();

  // Make API request to get tweets
  $.get('http://twitter-mock-timeline.com/home_timeline', {
    user_id: 1,  // Replace with actual user ID
    page: page
  }).done(function(tweets) {
    // Append tweets to timeline
    for (var i = 0; i < tweets.length; i++) {
      var tweet = tweets[i];
      $('#timeline').append(
        '<div class="tweet">' +
          '<div class="body">' + tweet.tweet_body + '</div>' +
          '<div class="username">' + tweet.user_id + '</div>' +
        '</div>'
      );
    }

    // Increment page and set loading to false
    page++;
    loading = false;

    // Hide loading indicator
    $('#loading').hide();
  });
}

// Load initial tweets
getTweets();

// On scroll, load more tweets
$(window).scroll(function() {
  if ($(window).scrollTop() + $(window).height() == $(document).height()) {
    getTweets();
  }
});

