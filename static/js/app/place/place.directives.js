var app = angular.module('place.directives', []);


app.directive('pSlider', ['$timeout',function($timeout){
	// Runs during compile
	return {
		require: 'ngModel',
		restrict: 'A',
		link: function($scope, iElm, iAttrs, ngModelCtrl) {
			var step = parseInt(iAttrs.step) || 1;
			iElm.slider({
				max: parseInt(iAttrs.max),
				min : parseInt(iAttrs.min),
				step: step,
				range:true,
				values : [iAttrs.min,iAttrs.max]
			});


			// third party notification of the directive change
			ngModelCtrl.$render = function() {
				iElm.slider( "values", ngModelCtrl.$viewValue);
			};

			// When data changes outside of AngularJS
			iElm.on('slidechange', function(event, ui) {
				$timeout(function() {
					ngModelCtrl.$setViewValue(iElm.slider("values"));
				},0);
			});
		}
	};
}]);