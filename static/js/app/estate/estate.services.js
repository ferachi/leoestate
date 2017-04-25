var app = angular.module('estate.services', []);

function Snackbar(){
	this._content="";
}
Snackbar.prototype.show = function (content) {
	this._content = content;
};