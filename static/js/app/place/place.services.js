/**
 * Module PlaceService
 *
 * @desc the services module for the module called Place
 * @type {Module}
 * @param {Resource} ngResource the module for serving the $resource service
 */
var app = angular.module('place.services',['ngResource']);


/**
 * Configuration
 * @desc Set PlaceService configuration
 * @param  {ResourceProvider} $resourceProvider the provider used to change $resource defaults
 */
app.config(['$resourceProvider', function($resourceProvider) {
	// django requires trailing slashes and the default
	// for angular is to strip trailing slashes
 	$resourceProvider.defaults.stripTrailingSlashes = false;
}]);


/**
 * PlaceFactory
 * @name  Place
 * @desc  Factory to load the list/detail of Place Object type as well as post, update and delete
 * @param {ResourceService} $resource the service used to serve the rest api
 */
app.factory('Place', ['$resource',function($resource){
	return $resource('/api/places/:slug/', {'slug':'@slug'})
}]);

/**
 * PlacesLoaderFactory
 * @name   Places Loader
 * @desc   this factory loads the list of places using the Place Factory defined earlier
 * @param  {deferred} $q angulars deferred type
 * @param  {PlaceResource} Place place resource object
 * @return {promise}
 */
app.factory('PlacesLoader', ['$q','Place', function($q,Place){
	return function(){
		var deferred = $q.defer();
		Place.query(function(places){
			deferred.resolve(places);
		},
		function(){
			deferred.reject('Unable to load the properties, try refreshing.');
		});
		return deferred.promise;
	}
}]);


/**
 * PlaceLoaderFactory
 * @name   Places Loader
 * @desc   this factory loads a single place using the Place Factory defined earlier
 * @param  {deferred} $q angulars deferred type
 * @param  {Route} $route the service used to provide routing and deeplinking URLS to views
 * @param  {PlaceResource} Place place resource object
 * @return {promise}
 */
app.factory('PlaceLoader', ['$q','$route','Place', function($q,$route,Place){
	return function(){
		var deferred = $q.defer();
		Place.get({slug:$route.current.params.slug},function(place){
			deferred.resolve(place);
		},
		function(){
			deferred.reject('Unable to load property,'+ $route.current.params.slug +' try refreshing.')
		});
		return deferred.promise;
	}
}])



/**
 * PropertyOptionsFactory
 * @name  Property Options
 * @desc  Factory to load the list of Property Options Object type 
 * @param {ResourceService} $resource the service used to serve the rest api
 */
app.factory('PropertyOptions', ['$http',function($http){
	return $http.get('/api/places/options/')
}]);

/**
 * OptionsLoaderFactory
 * @name   Options Loader
 * @desc   this factory loads the options used in the advanced search
 * @param  {deferred} $q angulars deferred type
 * @param  {PropertyOptions} PropertyOptions property options resource object
 * @return {promise}
 */
app.factory('OptionsLoader', ['$q','PropertyOptions', function($q,PropertyOptions){
	return function(){
		var deferred = $q.defer();
		PropertyOptions.then(function(config){
			deferred.resolve(config.data);
		},
		function(){
			console.log('error')
			deferred.reject('Unable to load the options, try refreshing.');
		});
		return deferred.promise;
	}
}]);