# ☁️ Google APIs (Maps, Geocoding)

At DataMade, we use several Google APIs to support our maps. Google continues to have the most robust [Geocoding service](https://developers.google.com/maps/documentation/geocoding/start) and we often times use the [Google Maps Javascript API](https://developers.google.com/maps/documentation/javascript/tutorial) for their map tiles as well.

To keep accurate accounting of API usage per website, we create a separate Google API key for each project.

DataMade staff have access to these keys here: https://console.developers.google.com/apis/credentials?folder=&organizationId=&project=adroit-hall-205721

### Creating a new Google API key

1. Navigate to the [Google API Console credentials page](https://console.developers.google.com/apis/credentials?folder=&organizationId=&project=adroit-hall-205721) and click 'Create credentials'.

2. Edit the API key and restrict access to HTTP Referrers. Add the list of allowed domains to the list. For local development, make sure to inclued `localhost` and `127.0.0.1`. 

3. In your app, add the API key any place the `maps.google.com/maps/api/js` script tag is called.

```html
<script type="text/javascript" src="https://maps.google.com/maps/api/js?sensor=false&libraries=places&key=YOUR_KEY_HERE"></script>
```

4. Deploy the changes and test that they work.

