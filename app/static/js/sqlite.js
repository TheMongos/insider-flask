try {
	if (!window.openDatabase) {
		alert('not supported');
	} 
	else {
		var shortName = 'insider';
		var version = '1.0';
		var displayName = 'insider db';
        var maxSize = 65536; // in bytes
        var database = openDatabase(shortName, version, displayName, maxSize);
    }
} catch(e) {
	if (e == 2) {
		// Version number mismatch.
		alert("Invalid database version.");
	} else {
		alert("Unknown error " + e + ".");
	}
	//return;
}


function showError(transaction, error)
{
	//console.log("error occured: this = " + this);//error.message+" error.code:"+error.code);
return true;
}

function nullDataHandler(transaction, results) 
{
	//console.log("nullDataHandler = " + this); 
}

// Create table
database.transaction(
	function( transaction ){
		transaction.executeSql("CREATE TABLE IF NOT EXISTS Following (" +
			"user_id INTEGER NOT NULL PRIMARY KEY ," +
			"username TEXT NOT NULL);");

		console.log("Following created");

		transaction.executeSql("CREATE TABLE IF NOT EXISTS Follower (" +
			"user_id INTEGER NOT NULL PRIMARY KEY ," +
			"username TEXT NOT NULL);");

		console.log("Followers created");

	},nullDataHandler,showError
	);

//  save a Follower.
var saveFollower = function(user_id, username, callback ){
	// Insert a new Follower.
	database.transaction(
		function( transaction ){
			// Insert a new Follower with the given values.
			transaction.executeSql(("INSERT INTO Follower (user_id,username) VALUES ( ?,?);"),
				[user_id,username],
				function( transaction, results ){
					// Execute the success callback,
					callback( results );
				}
				);
			console.log("db insert success");
		}
		,nullDataHandler,showError);
};

var saveFollowing = function(user_id, username, callback ) {
	// Insert a new Following.
	database.transaction(
		function( transaction ){
			// Insert a new Following with the given values.
			transaction.executeSql(("INSERT INTO Following (user_id,username) VALUES ( ?,?);"),
				[user_id,username],
				function( transaction, results ){
					// Execute the success callback,
					callback( results );
				}
				);
			console.log("db insert success");

		}
		,nullDataHandler,showError);
};

//save a Followers.
var saveFollowers = function(userArr, callback ) {
	var i;
	for (i = 0 ; i < userArr.length ; i++){
		saveFollower(userArr[i].user_id, userArr[i].username, function() {});
	}
};

// I get all the Follower.
var getFollower = function( callback ){
	// Get all the Follower.
	database.transaction(
		function( transaction ){

			// Get all the Follower in the table.
			transaction.executeSql(
				(
					"SELECT " +
					"* " +
					"FROM " +
					"Follower " +
					"ORDER BY " +
					"username ASC"
					),
				[],
				function( transaction, results ){
					// Return the Follower results set.
					callback( results );
				}
				);
			console.log("db select");

		}
		);
};

// I get all the Following.
var getFollowing = function( callback ){
	// Get all the Following.
	database.transaction(
		function( transaction ){

			// Get all the Following in the table.
			transaction.executeSql(
				(
					"SELECT " +
					"* " +
					"FROM " +
					"Following " +
					"ORDER BY " +
					"username ASC"
					),
				[],
				function( transaction, results ){
					// Return the Following results set.
					callback( results );
				}
				);
			console.log("db select");

			}
			);
	};

   // I delete all the Follower.
   var deleteFollowers = function( callback ){
		// Get all the Follower.
	database.transaction(
		function( transaction ){

			// Delete all the Follower.
			transaction.executeSql(
				("DELETE FROM Follower "),
				[],
				function(){	callback();	}
				);
			console.log("db delete Follower list");
		}
		);
};

// I delete all the Following.
var deleteFollowings = function( callback ){
	// Get all the Following.
	database.transaction(
		function( transaction ){

			// Delete all the Following.
			transaction.executeSql(
				("DELETE FROM Following "),
				[],
				function(){	callback();	}
				);
			console.log("db delete Following list");
		}
		);
};
