<?php 

function getData(){
	$data = unserialize(file_get_contents('data/dailyid'));

	$today = date("Ymd");
	
	if($data === false || $data['date'] != $today){
		$data['date'] = $today;
		$data['dailyid'] = uniqid();
		$data['tally'] = Array();
		file_put_contents('data/dailyid', serialize($data));
	}
	
	return $data;
}

$data = getData();
$userid = hash("sha256", $_SERVER['REMOTE_ADDR'].$data['dailyid']);

if(array_key_exists($userid, $data['tally'])){
	$data['tally'][$userid]++;
} else {
	$data['tally'][$userid] = 1;
}

// max. 20 datasets per day per IP
if($data['tally'][$userid] > 20){
	print("nu is aber auch ma jut.");
	die();
} else {
	file_put_contents('data/dailyid', serialize($data));

	$indexes = Array('q1','q2_fsem','q2_lp','q3','q4','q5','q6','q7','q8');

	$subindexes = Array('q5' => Array('q5-failed-admission',
				'q5-failed-module',
				'q5-moved-module',
				'q5-minor-subject',
				'q5-dependencies',
				'q5-grade-improvement',
				'q5-modules-o-plenty',
				'q5-pg2',
				'q5-long-project-group',
				'q5-thesis-problems',
				'q5-job',
				'q5-family',
				'q5-planned',
				'q5-other'
				),
			'q6' => Array('q6-failed-admission',
				'q6-failed-module',
				'q6-moved-module',
				'q6-minor-subject',
				'q6-dependencies',
				'q6-grade-improvement',
				'q6-modules-o-plenty',
				'q6-pg2',
				'q6-long-project-group',
				'q6-thesis-problems',
				'q6-job',
				'q6-family',
				'q6-planned',
				'q6-other'
				)
			);

	foreach($indexes as $index){
		if (!isset($_POST[$index])){
			print("invalid data");
			die();
		}
	}

	foreach($subindexes as $index){
		foreach($subindexes[$index] as $subindex){
			if (!isset($_POST[$index][$subindex])){
				print("invalid data");
				die();
			}
			if (!isset($_POST[$index][$subindex]['checked'])){
				print("invalid data");
				die();
			}
			if (!isset($_POST[$index][$subindex]['extra'])){
				print("invalid data");
				die();
			}
		}
	}


	$_POST['timestamp'] = time();
	$_POST['userid'] = $userid;

	$encoded = json_encode($_POST);
	$filename = "data/".uniqid().".json";
	file_put_contents($filename, $encoded);

	print("Gespeichert.");
}

?>