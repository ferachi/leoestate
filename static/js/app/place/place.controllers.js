var app = angular.module('place.controllers', []);

app.controller('PlaceListCtrl', ['places','$scope','$filter', 'options',function(places,$scope,$filter, options){
	$scope.title = "Places";
    $scope.places = places;
    $scope.options = options;
	$scope.searchExp = function(){};	// this is where the filter get's it's values from
    $scope.isList = true; // if the property list pane is displayed
    $scope.showDetail  = function(isList, place){
        $scope.isList = isList;
        $scope.place = $scope.isList ? {} : place;
    };
    
	$scope.$watch('searchExp', function(n,o){
		console.log('hello');
	});
}]);

app.controller('PlaceViewCtrl', ['place',function(place){
	this.place = place;
}]);


app.value('MockData', [
    {
        "slug": "la-grunge",
        "rentableplace": {
            "id": 1,
            "title": "la grunge",
            "slug": "la-grunge",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "price": "2000.00",
            "age": "o",
            "no_rooms": 4,
            "area": 200,
            "thumbnail": "http://localhost:9000/media/places/images/la-grunge/main/la_grunge_yGqrQAw.jpg",
            "image": "http://localhost:9000/media/places/images/la-grunge/thumbnail/la_grunge_i13gLfg.jpg",
            "created_date": "2017-03-12T15:00:36.391740Z",
            "timestamp": "2017-03-12T15:00:36.391740Z",
            "duration": 1,
            "is_rented": false,
            "duration_type": "m",
            "total_duration_months": null,
            "property_type": 1,
            "uploaded_by": 2,
            "facilities": [
                1
            ],
            "other_fields": []
        },
        "buyableplace": null,
        "images": [],
        "address": null,
        "three_d_views": []
    },
    {
        "slug": "kappa",
        "rentableplace": null,
        "buyableplace": {
            "id": 2,
            "title": "k'appa",
            "slug": "kappa",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "price": "50000.00",
            "age": "n",
            "no_rooms": 7,
            "area": null,
            "thumbnail": "http://localhost:9000/media/places/images/kappa/main/kappa.jpg",
            "image": "http://localhost:9000/media/places/images/kappa/thumbnail/kappa.jpg",
            "created_date": "2017-03-12T15:04:05.596773Z",
            "timestamp": "2017-03-12T15:04:05.596773Z",
            "is_sold": false,
            "property_type": 2,
            "uploaded_by": 1,
            "facilities": [
                1,
                2,
                4,
                5
            ],
            "other_fields": []
        },
        "images": [
            {
                "id": 1,
                "title": "kappa front view",
                "description": "front view of kappa",
                "image": "http://localhost:9000/media/places/images/kappa/images/kappa_front_view.jpg",
                "place": 2
            },
            {
                "id": 2,
                "title": "kappa sideview",
                "description": "side view for kappa",
                "image": "http://localhost:9000/media/places/images/kappa/images/kappa_sideview.jpg",
                "place": 2
            }
        ],
        "address": {
            "id": 1,
            "house_no": 6,
            "street": "simala rue",
            "city": "Nice",
            "town": "",
            "location": "France",
            "latitude": "4.59405964",
            "longitude": "10.34858430",
            "place": 2
        },
        "three_d_views": []
    }
])