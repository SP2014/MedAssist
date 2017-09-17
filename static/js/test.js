var myApp = angular.module('myApp', ['ngMaterial']);


myApp.directive('apsUploadFile', apsUploadFile);

function apsUploadFile() {
  var directive = {
    restrict: 'E',
    template: '<input id="fileInput" type="file" file-model="myFile" class="ng-hide"/> <md-button id="uploadButton" class="upBtn" aria-label="attach_file"><md-icon md-svg-src="http://127.0.0.1:5000/static/images/img_add.svg"></md-icon></md-button> <md-button class="subBtn" aria-label="attach_file" ng-click="uploadFile()" style="margin-top-20px;">Submit</md-button>',
    link: apsUploadFileLink
  };
  return directive;
};

function apsUploadFileLink(scope, element, attrs) {
  var input = $(element[0].querySelector('#fileInput'));
  var button = $(element[0].querySelector('#uploadButton'));

  button.click(function(e) {
      input.click();
  });

  input.on('change', function(e) {
    var files = e.target.files;
    if (files[0]) {
      scope.imgFile = files;
      scope.fileName = files[0].name;
      
    } else {
      scope.fileName = null;
    }
    scope.$apply();
  });
};

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl,doneCallback){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
		 .then(function (resp) {
           doneCallback(resp.data); // when the async http call is done, execute the callback
         });
    }
}]);


myApp.service('Query', ['$http', function ($http) {
    this.fetchQuery = function(dname,dlink, doneCallback){
        $http.get(dlink+dname)
		 .then(function (resp) {
           doneCallback(resp.data); // when the async http call is done, execute the callback
         });
    }
}]);







myApp.controller('myCtrl', ['$scope', 'fileUpload','Query', function($scope, fileUpload,Query){
    
	$scope.diseaseName = "";
	$scope.resultData = {};
	$scope.msg = "Welcome to MedAssist. You can ask your health related problems and we are here to help you. "
	$scope.showPicture = false;
	
	$scope.description = "";
	
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        if(file){
		  console.log('file is ' );
          console.dir(file);
          var uploadUrl = "/imageProcess";
		  $scope.showProgress = true;

		  fileUpload.uploadFileToUrl(file, uploadUrl, function (data) {
			console.log(data);
			if(data!=null){
			$scope.showProgress = false;
            $scope.diseaseName = data.result;
			
			Query.fetchQuery(data.result,'/data/',function(data){
				$scope.resultData = data;
				$scope.showPicture = true;
				$scope.msg = "Based on the image you submitted, our system predicts that you may be having " + $scope.diseaseName+". Here is some information about it"
			})
			
			}
          });
          		  
		}
		else{
			if($scope.description!=""){
			    Query.fetchQuery(data.result,'/data/',function(data){
				$scope.resultData = data;
				$scope.showPicture = true;
				$scope.msg = "Based on the image you submitted, our system predicts that you may be having " + $scope.diseaseName+". Here is some information about it"
			})
			}
		}
    };

    $scope.title = "MedAssist";
	
	$scope.showProgress = false;

    $scope.todos = [
      {
       "name":"Item 1",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 2",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 3",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 4",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 5",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 6",
       "content":"Some demo content",
       "selected":false
      },{
       "name":"Item 7",
       "content":"Some demo content",
       "selected":false
      }
    ];
    
}]);