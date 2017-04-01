<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Professor's appointments</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" media="screen" title="no title" charset="utf-8">
  		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	    <link href="style.css" rel="stylesheet">
    </head>
    <body>
		<div class="container">
			<nav class="navbar navbar-inverse">
				<div class="container-fluid">
					<div class="navbar-header">
			    		<a class="navbar-brand">Professor</a>
			 		</div>
				    <ul class="nav navbar-nav">
				    </ul>
				    <ul class="nav navbar-nav navbar-right">
				    	<li><a href="logOut.php"><span class="glyphicon glyphicon-log-out"></span>Log Out</a></li>
				    </ul>
			  	</div>
			</nav>

			<div class="jumbotron" style="background-color:#007dc6">
		        <h1 style="color:#ffc220">Professor</h1> 
		        <p class="lead">Here you can create your schedule and view your appointments</p>
			</div>
	        	<div class="row placeholders">
		            <div class="col-sm-3 placeholder" >
			            <a href="makeSchedule.php">
				              <img src="../img/cita.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>Make your schedule</h4>
			             </a>
		            </div>
		            <div class="col-sm-3 placeholder" >
			            <a href="makeAppointment.php">
				              <img src="../img/appo.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>Confirm appointment hour</h4>
			             </a>
		            </div>
		            <div class="col-sm-3 placeholder" >
			            <a href="showWeek.php">
				              <img src="../img/week.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>View your week</h4>
			             </a>
		            </div>
		            <div class="col-sm-3 placeholder" >
			            <a href="showMonth.php">
				              <img src="../img/month.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>View your month</h4>
			             </a>
		            </div>
		            <div class="col-sm-3 placeholder" >
			            <a href="makeExtrahelp.php">
				              <img src="../img/extra.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>Make your Extra-help</h4>
			             </a>
		            </div>
		            <div class="col-sm-3 placeholder" >
			            <a href="dateRange.php">
				              <img src="../img/range.png" width="200" height="200" class="img-responsive" alt="Generic placeholder thumbnail">
				              <h4>View appointments in a range</h4>
			             </a>
		            </div>
		             
	        	</div>
	        	<footer class="footer">
			    	<br><br><br><br>
			        <p>ITESM Campus Puebla</p>
			    </footer>
	    </div>
    </body>
</html>