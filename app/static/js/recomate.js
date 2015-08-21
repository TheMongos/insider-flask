var myApp = angular.module('recomate', ['ngRoute', 'ngResource', 'ngFileUpload', 'ngDialog']);

myApp.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider){

	$routeProvider
	.when('/top', {
		templateUrl: 'static/partials/top.html',
		controller: 'top'
	})
	.when('/search', {
		templateUrl: 'static/partials/search.html',
		controller: 'search'
	})
	.when('/admin/search', {
		templateUrl: 'static/partials/adminSearch.html',
		controller: 'search'
	})
	.when('/admin/item/:item_id', {
		templateUrl: 'static/partials/updateItem.html',
		controller: 'changeItem'
	})
	.when('/item/:item_id', {
		templateUrl: 'static/partials/item.html',
		controller:'item'
	})
	.when('/user/:user_id', {
		templateUrl: 'static/partials/user.html',
		controller:'user'
	})
	.when('/user/', {
		templateUrl: 'static/partials/user.html',
		controller:'user'
	})
	.when('/following/:username', {
		templateUrl: 'static/partials/following.html',
		controller:'following'
	})
	.when('/followers/:username', {
		templateUrl: 'static/partials/followers.html',
		controller:'followers'
	})
	.when('/login', {
		templateUrl: 'static/partials/login.html',
		controller:'login'
	})
	.when('/signup', {
		templateUrl: 'static/partials/signup.html',
		controller:'signup'
	})
	.when('/', {
		templateUrl: 'static/partials/user.html',
		controller:'user'
	});
}]);

myApp.controller('login', function($scope,$resource, $location){
	$('#navigator').css("display","none");
	var Login = $resource('/login');
	$scope.login = function (){
		$scope.message ="";
		$scope.messageShow = false;
		var obj = {username: $scope.username, password: $scope.password};
		Login.save(obj, function(res){
			$('#navigator').css("display","block");
			$location.path('/user').replace();
		},
		function(error){
			console.log(error);
			if(error.status == 401){
				$scope.message = error.data.message;
				$scope.messageShow = true;
			}

		});

	};
});

myApp.controller('signup', function($scope,$resource, $location){
	$('#navigator').css("display","none");
	var Login = $resource('/signup');
	$scope.signup = function (myForm){
		console.log(myForm);
		if(myForm.emailField.$valid == false){
			$scope.message = "email incorrect";
			$scope.errorShow = true;
		} else if ($scope.password != $scope.repassword) {
			$scope.message = "passwords don't match. try again";
			$scope.password = $scope.repassword = "";
			$scope.errorShow = true;
			$("#passwordDiv").addClass("has-error");
		} else if(myForm.$valid == false){
			$scope.message = "can't leave fields empty";
			$scope.errorShow = true;
		} else {
			$scope.message ="";
			$scope.errorShow = false;
			$("#passwordDiv").removeClass("has-error");
			var obj = {username: $scope.username, password: $scope.password, first_name: $scope.first_name, last_name: $scope.last_name, email: $scope.email};
			Login.save(obj, function(res){
				$('#navigator').css("display","block");
				$location.path('/login').replace();
			},
			function(error){
				if(error.status == 409){
					$scope.message = error.data.message;
					$scope.errorShow = true;
				}
			});
		}
	};
});


myApp.controller('user', function($scope, $resource, $location, $routeParams, Upload, ngDialog){

	var User;
	if($routeParams.user_id){
		User = $resource('/user/:user_id', {user_id: $routeParams.user_id});
	} else {
		User = $resource('/user/');
	}

	User.get(function(res){
		$scope.res = res;
		$scope.user = res.user;
		//$scope.userDetails = res.user.userDetails;
		$scope.currDate = (new Date()).getTime();

		getRanks(res.user.username);
		if(res.user.isMyAccount){
			$scope.showIfMyUser = true;
		} else {
			if(res.user.isFollowing) {
				$scope.followingLabel = "Following";
				$('#follow').addClass("follow");
				$('#follow').addClass("btn-success");
			} else {
				$scope.followingLabel = "Follow";
				$('#follow').addClass("notfollow");
				$('#follow').addClass("btn-primary");
			}
		}



	}, function (error){
		$location.path('/login').replace();
	});

	function getRanks(username){
		var Ranks = $resource('/rank/:username', {username: username});
		$scope.ranksArr =  Ranks.query();
	}

	$scope.getReview = function(index, item_id){
		var str2 = "review"+item_id;
		var reviewBtn = "#reviewBtn"+item_id;
		$(".reviewBtn").css("background-color","white");
		if ($scope.ranksArr[index].isOpen){
			$scope[str2] = false;
			$scope.ranksArr[index].isOpen = false;
			$(reviewBtn).html("read review");
		} else {
			$(reviewBtn).html("close review");
			$scope[str2] = true;
			$scope.ranksArr[index].isOpen = true;
		}
	};

	$scope.startFollowing = function(username){
		if(!$scope.user.isFollowing){
			var Follow = $resource('/user/follow/:username', {username: username});
			Follow.save(function(res){
				if(res.status == "success"){
					$scope.followingLabel = "Following";
					$('#follow').removeClass("notfollow btn-primary").addClass("follow btn-success");
					$scope.user.userFollowersCount++;
				}
			}, function (error){
				$location.path('/login').replace();
			});
		}
	}

	$scope.logout = function(){
		var Logout = $resource('/logout');

		Logout.save(function(res){
			$location.path('/login').replace();
		}, function (error){
			$location.path('/login').replace();
		})
	}


	$scope.admin = function (){
		$location.path('/admin/search').replace();
	}

	$scope.upload = function (files) {
        if (files && files.length == 1) {
            var file = files[0];
            $scope.preview = file;
            Upload.upload({
                url: '/upload',
                file: file
            }).progress(function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            }).success(function (data, status, headers, config) {
                console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            }).error(function (data, status, headers, config) {
                console.log('error status: ' + status);
            })
        }
    };

});

myApp.controller('changeItem', function($scope,$resource, $location, $routeParams){
	var Item = $resource('/item/:item_id', {item_id: $routeParams.item_id});
	Item.get(function(res){
		$scope.item = res;
		// $scope.title = res.itemDetails.title;
	}, function (error){
		$location.path('/login').replace();
	});


	$scope.changeItem = function (key, value){
		var Update = $resource('/admin/updateItem/:item_id/:key/:value', {item_id: $routeParams.item_id, key : key, value : value});
		Update.save(function(res){
			console.log(res);
			$scope.errorShow = true;
			$scope.message = res.message;
		}, function(error){
			$location.path('/login').replace();
		});
	}
});

myApp.controller('item', function($scope,$resource, $location, $routeParams){
	$(".input-rank").rating({min:0, max:5, step:0.01, size:'xs', disabled:true, showClear:false, showCaption:false, starCaptions:{0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',}});
	$("#input-user-rank").rating({min:0, max:5, step:1, size:'xs', showClear:false, showCaption:false, starCaptions:{0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',}});
	var Item = $resource('/item/:item_id', {item_id: $routeParams.item_id});
	Item.get(function(res){
		$scope.item = res;
		console.log($scope.item);
		$scope.reviewButton = "write review";


		if (!$scope.item.itemDetails.hasOwnProperty('poster_path')) {
			$scope.item.itemDetails.poster_path = false;
		}

		if (res.itemRanks.rank) {
			$('#input-user-rank').rating('update', res.itemRanks.rank);
			$('#input-user-rank').on('rating.change', function(event, value, caption) {
				console.log("rating.change");
				 $scope.myRank = value;
				 $scope.addRank();
			});
			$scope.myRank = res.itemRanks.rank;
			$scope.reviewText = res.itemRanks.review_text;
		} else {
			$scope.myRank = 0;
		}

		$("#followingAvgRank").rating('update', $scope.item.itemRanks.followingAvg);
		$("#totalRank").rating('update', $scope.item.itemRanks.totalAvg);
		if($scope.item.itemRanks.followingAvg == null){
			$scope.item.itemRanks.followingAvg = '-';
		}

		if(!('poster_path' in $scope.item.itemDetails)){
			$scope.item.itemDetails.poster_path = null;
		}

		$scope.getFollowingRanks();
	}, function (error){
		$location.path('/login').replace();
	});


	$scope.showDescription = function() {
		if ($scope.description) {
			$scope.description = false;
		} else {
			$scope.description = true;
		}
	}

	$scope.addRankTest = function(){
		console.log("here");
		console.log($scope.myRank2);

	}

	$scope.addRank = function(){
		$scope.errorShow = false;
		$scope.message = "";
		if($scope.myRank != 0){
			var Rank = $resource('/rank/:item_id/:rank', {item_id: $scope.item.itemDetails.item_id , rank: $scope.myRank});
			Rank.save(function(res){
				console.log(res);
			},
			function (error){
				$location.path('/login').replace();
			});
		}
	}



	$scope.addReview = function(){
		$(".reviewBtn").css("background-color","white");
		if($scope.showReview){
			$scope.reviewButton = "write review";
			$scope.showReview =false;
			$scope.hideItem = false;
		} else {
			$scope.reviewButton = "close review";
			$scope.showReview =true;
			$scope.hideItem = true;
		}
	}

	$scope.sendReview = function(){
		if($scope.reviewText) {
			if($scope.myRank != 0 && $scope.myRank){
				var obj = {item_id: $scope.item.itemDetails.item_id, category_id: $scope.item.itemDetails.category_id , rank: $scope.myRank, review_text: $scope.reviewText};
				var Rank = $resource('/review');
				Rank.save(obj, function(res){
					$scope.getReview(res.review_id);
					$scope.userRank.review_id = res.review_id;
				},
				function (error){
					$location.path('/login').replace();
				});
				$scope.addReview();
			} else {
				$scope.errorShow = true;
				$scope.message = "please rank the title";
			}
		}
	}

	$scope.getFollowingRanks = function(){
		var Rank = $resource('/rank/following/:item_id', {item_id : $scope.item.itemDetails.item_id});
		$scope.ranksArr = Rank.query(function(res){
			console.log(res);
		},
		function (error){
			$location.path('/login').replace();
		});
	}

	$scope.getReview = function(index, username){
		var str2 = "review"+username;
		var reviewBtn = "#reviewBtn"+username;
		$(".reviewBtn").css("background-color","white");
		if ($scope.ranksArr[index].isOpen){
			$scope[str2] = false;
			$scope.ranksArr[index].isOpen = false;
			$(reviewBtn).html("read review");
		} else {
			$(reviewBtn).html("close review");
			$scope[str2] = true;
			$scope.ranksArr[index].isOpen = true;
		}
	};

	$scope.deleteReview = function() {
		var Delete = $resource('/review/:item_id', { item_id: $scope.item.itemDetails.item_id });

		Delete.remove(function(res){
			$scope.review_text = "";
			// $scope.userRank.review_id = "";
		},
		function (error){
			$location.path('/login').replace();
		});
	}



});

myApp.controller('top', function($scope,$resource, $location, $routeParams){
	$scope.categories = [
	                     {label:'Movie'},
	                     {label:'TV'}
	                     ];

	var Genres = $resource('/item/genres');
		$scope.genreArr = Genres.query(function(res) {
			$scope.genreArr.unshift('All');
			$scope.selectedGenre = $scope.genreArr[0];
		}, function(error) {
			$location.path('/login').replace();
		});

	$scope.selectedCat = $scope.categories[0];
	$scope.showFollowing = true;

	$scope.changeCategory = function() {
		if ($scope.showFollowing) {
			$scope.getTopFollowing();
		} else {
			$scope.getTopAll();
		}
	}

	$scope.changeGenre = function() {
		if ($scope.showFollowing) {
			if ($scope.selectedGenre == 'All') {
				$scope.getTopFollowing();
			} else {
				$scope.getTopFollowing($scope.selectedGenre);
			}
		} else {
			if ($scope.selectedGenre == 'All') {
				$scope.getTopAll();
			} else {
				$scope.getTopAll($scope.selectedGenre);
			}

		}
	}

	$scope.getTopAll = function(genre) {
		$scope.showFollowing = false;

		//activation check
		var All = $resource('/best/:label/:genre', { label : $scope.selectedCat.label, genre : genre });
		$scope.itemsArr = All.query(function(res) {
			console.log(res);
		}, function(error) {
			$location.path('/login').replace();
		});
	}

	$scope.getTopFollowing = function(genre) {
		$scope.showFollowing = true;

		var Following = $resource('/best/following/:label/:genre', { label : $scope.selectedCat.label, genre : genre });
		$scope.itemsArr = Following.query(function(res) {
			console.log(res);
		}, function(error) {
			$location.path('/login').replace();
		});
	}

	//initial
	$scope.getTopFollowing();

});

myApp.controller('search', function($scope,$resource, $location, $routeParams){
	$scope.isMovie = true;

	$scope.changeSearch = function(clicked){
		var isUserTemp;
		if (clicked == "tv"){
			isUserTemp = $scope.isUser;
			$scope.isTv = true; $scope.isMovie = false; $scope.isUser = false;
		} else if (clicked == "movie"){
			isUserTemp = $scope.isUser;
			$scope.isMovie = true; $scope.isTv = false; $scope.isUser = false;
		} else if (clicked == "user"){
			$scope.isUser = true; $scope.isMovie = false; $scope.isTv = false;
			$scope.search();
		}

		if(isUserTemp){
			$scope.search();
		}
	}

	$scope.search = function(){
		if (typeof $scope.searchText != 'undefined') {
			$scope.userArr = $scope.itemArr = null;
			$scope.loading = true;
		}

		if($scope.searchText) {
			if ($scope.isUser) {
				var SearchUser = $resource('/search/user/:query', { query : $scope.searchText });

				SearchUser.query(function(res) {
					$scope.userArr = res;
					console.log(res);
					// do something
				}, function(error) {
					$location.path('/login').replace();
				}).$promise.finally(function() {
					$scope.loading = false;
				});
			} else {
				var SearchItem = $resource('/search/item/:query', { query : $scope.searchText });

				SearchItem.query(function(res) {
					$scope.itemArr = res;
					console.log(res);
					// do something
				}, function(error) {
					$location.path('/login').replace();
				}).$promise.finally(function() {
					$scope.loading = false;
				});
			}
		}
	}

	$scope.$on('ALWAYS', function() {
		//$scope.loading = false;
    	});
});

myApp.controller('following', function($scope,$resource, $location, $routeParams){
	var Following = $resource('/user/following/:username', {username: $routeParams.username});

	$scope.followArr = Following.query(function(res){
		console.log(res);
	},
	function (error){
		$location.path('/login').replace();
	});

});

myApp.controller('followers', function($scope,$resource, $location, $routeParams){
	var Followers = $resource('/user/followers/:username', {username: $routeParams.username});
	$scope.followArr = Followers.query(function(res){
		console.log(res);
	},
	function (error){
		$location.path('/login').replace();
	});

});

myApp.directive('starRank', function() {
  return {
    link: function(scope, element, attrs) {
		var size = 'xs';
		if(typeof(attrs.rankSize) !== 'undefined'){
			console.log("rankSize " + attrs.rankSize);
			size = attrs.rankSize;
		}
		element.rating({
			min: 0,
			max: 5,
			step: 0.01,
			size: size,
			readonly: true,
			showClear: false,
			showCaption: false,
			starCaptions: {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5',}
		});
		element.rating('update', attrs.starRank);

		var height = element.parent().parent()[0].offsetHeight;
		var width = element.parent().parent()[0].offsetWidth;
		element.parent().parent().parent().append('<div class="warp-stars" style="height: '+height+'px;width: '+width+'px;"></div>')

    }
  }
});

myApp.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (typeof(attrs.src) != 'undefined' && attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  }
});

myApp.controller('addItem', function($scope,$resource, $location, $routeParams){

	var Followers = $resource('/addItem/followers/:username', {username: $routeParams.username});

	$scope.followArr = Followers.query(function(res){
		console.log(res);
	},
	function (error){
		$location.path('/login').replace();
	});
});
