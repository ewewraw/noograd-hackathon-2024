export const authenticate = function() {
      chrome.identity.getAuthToken({interactive: true}, function(token) {
        console.log(token);
      });
  };


 