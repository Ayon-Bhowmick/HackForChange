#import <GoogleMaps/GoogleMaps.h>
#import <React/RCTRootView.h>

@implementation AppDelegate
...

(BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
+  [GMSServices provideAPIKey:@" AIzaSyAwDCdf88Yq2ZroapxOY-FyfxEvBN0Ymx8"]; // add this line using the api key obtained from Google Console
...
