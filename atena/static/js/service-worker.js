function focusWindow(event) {
  /**** START notificationFocusWindow ****/
  /**** START urlToOpen ****/
  const urlToOpen = new URL(event.notification.data.link, self.location.origin).href;
  /**** END urlToOpen ****/

  /**** START clientsMatchAll ****/
  const promiseChain = clients.matchAll({
    type: 'window',
    includeUncontrolled: true
  })
  /**** END clientsMatchAll ****/
  /**** START searchClients ****/
  .then((windowClients) => {
    let matchingClient = null;

    for (let i = 0; i < windowClients.length; i++) {
      const windowClient = windowClients[i];
      if (windowClient.url === urlToOpen) {
        matchingClient = windowClient;
        break;
      }
    }

    if (matchingClient) {
      return matchingClient.focus();
    } else {
      return clients.openWindow(urlToOpen);
    }
  });
  /**** END searchClients ****/

  event.waitUntil(promiseChain);
  /**** END notificationFocusWindow ****/
}

/**** START isClientFocused ****/
function isClientFocused() {
  return clients.matchAll({
    type: 'window',
    includeUncontrolled: true
  })
  .then((windowClients) => {
    let clientIsFocused = false;

    for (let i = 0; i < windowClients.length; i++) {
      const windowClient = windowClients[i];
      if (windowClient.focused) {
        clientIsFocused = true;
        break;
      }
    }

    return clientIsFocused;
  });
}
/**** END isClientFocused ****/

// function demoMustShowNotificationCheck(event) {
//   /**** START showNotificationRequired ****/
//   const promiseChain = isClientFocused()
//   .then((clientIsFocused) => {
//     if (clientIsFocused) {
//       console.log('Don\'t need to show a notification.');
//       return;
//
//     }
//
//     // Client isn't focused, we need to show a notification.
//     return self.registration.showNotification('Had to show a notification.');
//   });
//
//   event.waitUntil(promiseChain);
//   /**** END showNotificationRequired ****/
// }
//
// function demoSendMessageToPage(event) {
//   /**** START sendPageMessage ****/
//   const promiseChain = isClientFocused()
//   .then((clientIsFocused) => {
//     if (clientIsFocused) {
//       windowClients.forEach((windowClient) => {
//         windowClient.postMessage({
//           message: 'Received a push message.',
//           time: new Date().toString()
//         });
//       });
//     } else {
//       return self.registration.showNotification('No focused windows', {
//         body: 'Had to show a notification instead of messaging each page.'
//       });
//     }
//   });
//
//   event.waitUntil(promiseChain);
//   /**** END sendPageMessage ****/
// }
//
// self.addEventListener('push', function(event) {
//   if (event.data) {
//     switch(event.data.text()) {
//       case 'must-show-notification':
//         demoMustShowNotificationCheck(event);
//         break;
//       case 'send-message-to-page':
//         demoSendMessageToPage(event);
//         break;
//       default:
//         console.warn('Unsure of how to handle push event: ', event.data);
//         break;
//     }
//   }
// });
//
// /**** START notificationActionClickEvent ****/
// self.addEventListener('notificationclick', function(event) {
//   if (!event.action) {
//     // Was a normal notification click
//     console.log('Notification Click.');
//     return;
//   }
//
//   switch (event.action) {
//     case 'coffee-action':
//       console.log('User ❤️️\'s coffee.');
//       break;
//     case 'doughnut-action':
//       console.log('User ❤️️\'s doughnuts.');
//       break;
//     case 'gramophone-action':
//       console.log('User ❤️️\'s music.');
//       break;
//     case 'atom-action':
//       console.log('User ❤️️\'s science.');
//       break;
//     default:
//       console.log(`Unknown action clicked: '${event.action}'`);
//       break;
//   }
// });
// /**** END notificationActionClickEvent ****/

/**** START notificationClickEvent ****/
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  switch(event.notification.tag) {
    case 'focus-window':
      focusWindow(event);
      break;
    default:
      // NOOP
      break;
  }
});
/**** END notificationClickEvent ****/

const notificationCloseAnalytics = () => {
  return Promise.resolve();
};

/**** START notificationCloseEvent ****/
self.addEventListener('notificationclose', function(event) {
  const dismissedNotification = event.notification;

  const promiseChain = notificationCloseAnalytics();
  event.waitUntil(promiseChain);
});
/**** END notificationCloseEvent ****/

// self.addEventListener('message', function(event) {
//   console.log('Received message from page.', event.data);
//   switch(event.data) {
//     case 'must-show-notification-demo':
//       self.dispatchEvent(new PushEvent('push', {
//         data: 'must-show-notification'
//       }));
//       break;
//     case 'send-message-to-page-demo':
//       self.dispatchEvent(new PushEvent('push', {
//         data: 'send-message-to-page'
//       }));
//       break;
//     default:
//       console.warn('Unknown message received in service-worker.js');
//       break;
//   }
// });
