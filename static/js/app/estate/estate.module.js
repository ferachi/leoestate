/**
*  Module EstateApp
*
* @desc Applications Module
*/
var app = angular.module('EstateApp', ['ngRoute','ngAnimate', 'place', 'estate.directives']);



/**
 * Configuration
 * @desc Define valid application routes
 * 
 */
app.config(['$routeProvider', '$locationProvider',function($routeProvider, $locationProvider) {
	$routeProvider
	.when('/estate/',{
		controller:'PlaceListCtrl',
		controllerAs : 'ctrl',
		templateUrl:'/static/place/templates/place_list.html',
		resolve : {
			places : function(PlacesLoader){
				return PlacesLoader();
			},
			options : function(OptionsLoader){
				return OptionsLoader();
			}
		}
	})
	.when('/estate/view/:slug/',{
		controller:'PlaceViewCtrl',
		controllerAs : 'ctrl',
		templateUrl:'/static/place/templates/place_detail.html',
		resolve : {
			place : function(PlaceLoader){
				return PlaceLoader();
			}
		}
	})

	$locationProvider.html5Mode(true);
}]);



/**
 * MainController
 * @name Main Controller
 * @desc Main Application Controller
 * 
 */
app.controller('MainController', ['$scope', function($scope){
	$scope.title = "my title";
	
}]);





