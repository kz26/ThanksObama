app = angular.module 'app', ['ngSanitize']

app.factory 'questions', ($http) ->
	return {
		newQuestion: (cb) ->
			doRequest = ->
				$http.get('/new-question/')
					.success (data) ->
						cb(data)
					.error ->
						doRequest()
			doRequest()
	}

MainCtrl = ($scope, questions) ->
	$scope.numQuestions = 2
	$scope.currentQuestionNum = 0
	$scope.numCorrect = 0
	$scope.percentCorrect = 0

	$scope.getNextQuestion = ->
		if $scope.currentQuestionNum == $scope.numQuestions
			$scope.gameOver = true
			$scope.calculateGrade()
			return
		$scope.busy = true
		questions.newQuestion (data) ->
			$scope.currentQuestion = data
			$scope.currentQuestionNum++
			$scope.busy = false
	$scope.getNextQuestion() # get the first question

	$scope.setChoice = (i) ->
		$scope.choice = i 

	$scope.submitChoice = ->
		$scope.currentQuestion.graded = true
		$scope.currentQuestion.correct = ($scope.choice == $scope.currentQuestion.answer)
		if $scope.currentQuestion.correct
			$scope.numCorrect++
			$scope.percentCorrect = 100 * $scope.numCorrect / $scope.numQuestions


	$scope.getProgressBarStyle = ->
		color = "green"
		if $scope.percentCorrect < 50
			color = "red"
		else if $scope.percentCorrect < 70
			color = "yellow"
		else if $scope.percentCorrect < 90
			color = "orange"
		return {width: "#{ $scope.percentCorrect }%", 'background-color': color}

	$scope.calculateGrade = ->
		pc = $scope.percentCorrect
		if pc < 60
			$scope.letterGrade = "F"
			$scope.doctorLevel = "Bro, do you even healthcare?"
		else if pc < 70
			$scope.letterGrade = "D"
			$scope.doctorLevel = "Nurse Assistant"
		else if pc < 80
			$scope.letterGrade = "C"
			$scope.doctorLevel = "Nurse"
		else if pc < 90
			$scope.letterGrade = "B"
			$scope.doctorLevel = "Physician"
		else
			$scope.letterGrade = "A"
			$scope.doctorLevel = "Dr. House"
		 
