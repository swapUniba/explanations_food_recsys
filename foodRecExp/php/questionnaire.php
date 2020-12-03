<div class="form-group row">
	<div class="col-lg-6">
		<label class="question" for="Q1">Given the current information, which recipe you choose?</label>
	</div>	
	<div class="col-lg-6">
		<select class="form-control" id="Q1" name="Q1" required onchange="dynamicForm()">
			<!--<option hidden disabled selected value></option>-->
			<option hidden selected></option>
			<option value="left">Left side recipe</option>
			<option value="none">None of these two</option>
			<option value="right">Right side recipe</option>
		</select>
	</div>
</div>

<div class="row" id="labelPreQuest">
	<div class="col-lg-12">
		<h4>Why did you choose this recipe?</h4>
		<sub>Remember: <i>1 Star means completely disagree, 5 Stars mean completely agree</i></sub>
	</div>
</div>

<div class="form-group row" id="Q2div"> <!-- style="display: none;"-->
	<div class="col-lg-6">
		<label class="question" for="Q2">It matches my food tastes and preferences</label>
	</div>
	<div class="col-lg-6">
		<fieldset class="rating">					 			    
			<input type="radio" id="star5Q2" name="Q2" value="5" required/>
			<label class = "full" for="star5Q2" title="5 - completely agree"></label>
			
			<input type="radio" id="star4Q2" name="Q2" value="4" required/>
			<label class = "full" for="star4Q2" title="4 - agree"></label>
			
			<input type="radio" id="star3Q2" name="Q2" value="3" required/>
			<label class = "full" for="star3Q2" title="3 - neither agree or disagree"></label>
			
			<input type="radio" id="star2Q2" name="Q2" value="2" required/>
			<label class = "full" for="star2Q2" title="2 - disagree"></label>
			
			<input type="radio" id="star1Q2" name="Q2" value="1" required/>
			<label class = "full" for="star1Q2" title="1 - completely disagree"></label>
		</fieldset>
	</div>
</div>

<div class="form-group row" id="Q3div"> <!-- style="display: none;"-->
	<div class="col-lg-6">
		<label class="question" for="Q3">It seems savory and tastier</label>
	</div>
	<div class="col-lg-6">
		<fieldset class="rating">					 			    
			<input type="radio" id="star5Q3" name="Q3" value="5" required/>
			<label class = "full" for="star5Q3" title="5 - completely agree"></label>
			
			<input type="radio" id="star4Q3" name="Q3" value="4" required/>
			<label class = "full" for="star4Q3" title="4 - agree"></label>
			
			<input type="radio" id="star3Q3" name="Q3" value="3" required/>
			<label class = "full" for="star3Q3" title="3 - neither agree or disagree"></label>
			
			<input type="radio" id="star2Q3" name="Q3" value="2" required/>
			<label class = "full" for="star2Q3" title="2 - disagree"></label>
			
			<input type="radio" id="star1Q3" name="Q3" value="1" required/>
			<label class = "full" for="star1Q3" title="1 - completely disagree"></label>
		</fieldset>
	</div>
</div>

<div class="form-group row" id="Q4div">
	<div class="col-lg-6">
		<label class="question" for="Q4">It helps me to eat more healthily</label>
	</div>
	<div class="col-lg-6">
		<fieldset class="rating">					 			    
			<input type="radio" id="star5Q4" name="Q4" value="5" required/>
			<label class = "full" for="star5Q4" title="5 - completely agree"></label>
			
			<input type="radio" id="star4Q4" name="Q4" value="4" required/>
			<label class = "full" for="star4Q4" title="4 - agree"></label>
			
			<input type="radio" id="star3Q4" name="Q4" value="3" required/>
			<label class = "full" for="star3Q4" title="3 - neither agree or disagree"></label>
			
			<input type="radio" id="star2Q4" name="Q4" value="2" required/>
			<label class = "full" for="star2Q4" title="2 - disagree"></label>
			
			<input type="radio" id="star1Q4" name="Q4" value="1" required/>
			<label class = "full" for="star1Q4" title="1 - completely disagree"></label>
		</fieldset>
	</div>
</div>

<div class="form-group row" id="Q5div">
	<div class="col-lg-6">
		<label class="question" for="Q5">It would help me to lose/gain weight</label>
	</div>
	<div class="col-lg-6">
		<fieldset class="rating">					 			    
			<input type="radio" id="star5Q5" name="Q5" value="5" required/>
			<label class = "full" for="star5Q5" title="5 - completely agree"></label>
			
			<input type="radio" id="star4Q5" name="Q5" value="4" required/>
			<label class = "full" for="star4Q5" title="4 - agree"></label>
			
			<input type="radio" id="star3Q5" name="Q5" value="3" required/>
			<label class = "full" for="star3Q5" title="3 - neither agree or disagree"></label>
			
			<input type="radio" id="star2Q5" name="Q5" value="2" required/>
			<label class = "full" for="star2Q5" title="2 - disagree"></label>
			
			<input type="radio" id="star1Q5" name="Q5" value="1" required/>
			<label class = "full" for="star1Q5" title="1 - completely disagree"></label>
		</fieldset>
	</div>
</div>

<div class="form-group row" id="Q6div">
	<div class="col-lg-6">
		<label class="question" for="Q6">It seems easier to prepare</label>
	</div>
	<div class="col-lg-6">
		<fieldset class="rating">					 			    
			<input type="radio" id="star5Q6" name="Q6" value="5" required/>
			<label class = "full" for="star5Q6" title="5 - completely agree"></label>
			
			<input type="radio" id="star4Q6" name="Q6" value="4" required/>
			<label class = "full" for="star4Q6" title="4 - agree"></label>
			
			<input type="radio" id="star3Q6" name="Q6" value="3" required/>
			<label class = "full" for="star3Q6" title="3 - neither agree or disagree"></label>
			
			<input type="radio" id="star2Q6" name="Q6" value="2" required/>
			<label class = "full" for="star2Q6" title="2 - disagree"></label>
			
			<input type="radio" id="star1Q6" name="Q6" value="1" required/>
			<label class = "full" for="star1Q6" title="1 - completely disagree"></label>
		</fieldset>
	</div>
</div>

<div class="form-group row " id="Q7div">
    <div class="col-lg-6">
        <label class="question" for="Q7">I chose it because there was no other choice. </label>
    </div>
    <div class="col-lg-6 yes_no">
        <input type="checkbox" name="Q7" id="y" value="yes" />
        <label for="y">I would not have chosen any of these</label>
    </div>
</div>

<div class="form-group row" id="Q8div">
	<div class="col-lg-6">
		<label class="question" for="Q8">Other: </label>
	</div>
	<div class="col-lg-6">
		<textarea class="form-control" id="Q8" name="Q8" rows="2"></textarea>
	</div>
</div>

<!-- Main JS -->
<script>
	function dynamicForm(){
		var e = document.getElementById("Q1");
		var value = e.options[e.selectedIndex].text;
		if(value == "None of these two"){
			document.getElementById( 'Q2div' ).style.display = 'none';
			document.getElementById( 'Q3div' ).style.display = 'none';
			document.getElementById( 'Q4div' ).style.display = 'none';
			document.getElementById( 'Q5div' ).style.display = 'none';
			document.getElementById( 'Q6div' ).style.display = 'none';
			document.getElementById( 'Q7div' ).style.display = 'none';
			document.getElementById( 'labelPreQuest' ).style.display = 'none';

			document.getElementById( 'star5Q2' ).required = false;
			document.getElementById( 'star4Q2' ).required = false;
			document.getElementById( 'star3Q2' ).required = false;
			document.getElementById( 'star2Q2' ).required = false;
			document.getElementById( 'star1Q2' ).required = false;

			document.getElementById( 'star5Q3' ).required = false;
			document.getElementById( 'star4Q3' ).required = false;
			document.getElementById( 'star3Q3' ).required = false;
			document.getElementById( 'star2Q3' ).required = false;
			document.getElementById( 'star1Q3' ).required = false;

			document.getElementById( 'star5Q4' ).required = false;
			document.getElementById( 'star4Q4' ).required = false;
			document.getElementById( 'star3Q4' ).required = false;
			document.getElementById( 'star2Q4' ).required = false;
			document.getElementById( 'star1Q4' ).required = false;

			document.getElementById( 'star5Q5' ).required = false;
			document.getElementById( 'star4Q5' ).required = false;
			document.getElementById( 'star3Q5' ).required = false;
			document.getElementById( 'star2Q5' ).required = false;
			document.getElementById( 'star1Q5' ).required = false;
			
			document.getElementById( 'star5Q6' ).required = false;
			document.getElementById( 'star4Q6' ).required = false;
			document.getElementById( 'star3Q6' ).required = false;
			document.getElementById( 'star2Q6' ).required = false;
			document.getElementById( 'star1Q6' ).required = false;

            document.getElementById('y').required = false;
		} else {
			document.getElementById( 'Q2div' ).style.display = '';
			document.getElementById( 'Q3div' ).style.display = '';
			document.getElementById( 'Q4div' ).style.display = '';
			document.getElementById( 'Q5div' ).style.display = '';
			document.getElementById( 'Q6div' ).style.display = '';
			document.getElementById( 'Q7div' ).style.display = '';
			document.getElementById( 'labelPreQuest' ).style.display = '';

			document.getElementById( 'star5Q2' ).required = true;
			document.getElementById( 'star4Q2' ).required = true;
			document.getElementById( 'star3Q2' ).required = true;
			document.getElementById( 'star2Q2' ).required = true;
			document.getElementById( 'star1Q2' ).required = true;

			document.getElementById( 'star5Q3' ).required = true;
			document.getElementById( 'star4Q3' ).required = true;
			document.getElementById( 'star3Q3' ).required = true;
			document.getElementById( 'star2Q3' ).required = true;
			document.getElementById( 'star1Q3' ).required = true;

			document.getElementById( 'star5Q4' ).required = true;
			document.getElementById( 'star4Q4' ).required = true;
			document.getElementById( 'star3Q4' ).required = true;
			document.getElementById( 'star2Q4' ).required = true;
			document.getElementById( 'star1Q4' ).required = true;

			document.getElementById( 'star5Q5' ).required = true;
			document.getElementById( 'star4Q5' ).required = true;
			document.getElementById( 'star3Q5' ).required = true;
			document.getElementById( 'star2Q5' ).required = true;
			document.getElementById( 'star1Q5' ).required = true;
			
			document.getElementById( 'star5Q6' ).required = true;
			document.getElementById( 'star4Q6' ).required = true;
			document.getElementById( 'star3Q6' ).required = true;
			document.getElementById( 'star2Q6' ).required = true;
			document.getElementById( 'star1Q6' ).required = true;

            document.getElementById( 'y' ).required = false;

		}
	}
</script>