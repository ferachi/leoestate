var app = angular.module('estate.directives', []);

app.directive('loader', ['$rootScope',function($rootScope) {
    return {
        link: function(scope, element, attrs) {
            element.addClass('hide');
            $rootScope.$on('$routeChangeStart', function() {
                element.removeClass('hide');
            });
            $rootScope.$on('$routeChangeSuccess', function() {
                element.addClass('hide');
            });
        }
    };
}]);

app.directive('btn', [function() {
    return {
        restrict:'A',
        link: function(scope, element, attrs) {
            element.addClass('estate-btn');

            // look for i or span depending on which is used
            var $icon = element.find('i').length > 0 ? element.find('i'): element.find('span');

            if($icon.length>0){
                $icon.addClass('glower');
                if(attrs['helpText']){
                    var helpDiv = angular.element("<div id='snackbar' class='help-text'></div>");
                    helpDiv.html("<p>"+attrs['helpText']+"</p>");
                }

            }
        }
    };
}]);

app.directive('snackbar', ['$timeout',function($timeout) {
    return {
        restrict:'E',
        template: '<div id="snackbar" ><p>{{text}}</p></div>',
        scope:{
            text:'@',
            display: '@',
        },
        replace : true,
        link: function(scope, element, attrs, ctrl, transclude) {
        }
    };
}]);