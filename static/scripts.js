/* Counter */
window.addEventListener('resize', function(event){
    var newWidth = window.innerWidth;
    var newHeight = window.innerHeight; 
	if (newWidth < 420)
	{
		
	}
});
(function ($) {
	$.fn.countTo = function (options) {
		options = options || {};
		
		return $(this).each(function () {
			// set options for current element
			var settings = $.extend({}, $.fn.countTo.defaults, {
				from:            $(this).data('from'),
				to:              $(this).data('to'),
				speed:           $(this).data('speed'),
				refreshInterval: $(this).data('refresh-interval'),
				decimals:        $(this).data('decimals')
			}, options);
			
			// how many times to update the value, and how much to increment the value on each update
			var loops = Math.ceil(settings.speed / settings.refreshInterval),
				increment = (settings.to - settings.from) / loops;
			
			// references & variables that will change with each update
			var self = this,
				$self = $(this),
				loopCount = 0,
				value = settings.from,
				data = $self.data('countTo') || {};
			
			$self.data('countTo', data);
			
			// if an existing interval can be found, clear it first
			if (data.interval) {
				clearInterval(data.interval);
			}
			data.interval = setInterval(updateTimer, settings.refreshInterval);
			
			// initialize the element with the starting value
			render(value);
			
			function updateTimer() {
				value += increment;
				loopCount++;
				
				render(value);
				
				if (typeof(settings.onUpdate) == 'function') {
					settings.onUpdate.call(self, value);
				}
				
				if (loopCount >= loops) {
					// remove the interval
					$self.removeData('countTo');
					clearInterval(data.interval);
					value = settings.to;
					
					if (typeof(settings.onComplete) == 'function') {
						settings.onComplete.call(self, value);
					}
				}
			}
			
			function render(value) {
				var formattedValue = settings.formatter.call(self, value, settings);
				$self.html(formattedValue);
			}
		});
	};
	
	$.fn.countTo.defaults = {
		from: 0,               // the number the element should start at
		to: 0,                 // the number the element should end at
		speed: 1000,           // how long it should take to count between the target numbers
		refreshInterval: 100,  // how often the element should be updated
		decimals: 0,           // the number of decimal places to show
		formatter: formatter,  // handler for formatting the value before rendering
		onUpdate: null,        // callback method for every time the element is updated
		onComplete: null       // callback method for when the element finishes updating
	};
	
	function formatter(value, settings) {
		return value.toFixed(settings.decimals);
	}
}(jQuery));

jQuery(function ($) {
  // custom formatting example
  $('.count-number').data('countToOptions', {
	formatter: function (value, options) {
	  return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
	}
  });
  
  // start all the timers
  $('.timer').each(count);  
  
  function count(options) {
	var $this = $(this);
	options = $.extend({}, options || {}, $this.data('countToOptions') || {});
	$this.countTo(options);
  }
});

/* Counter end */


/* Form */
function student() {
	document.querySelector(".form2").style.display = "none";
	document.querySelector(".but2").style.color= "white";
	document.querySelector(".but2").style.backgroundColor= "#007bff";
	document.querySelector(".form1").style.display = "block";
	document.querySelector(".but1").style.color= "black";
	document.querySelector(".but1").style.backgroundColor= "white";
}

function teacher() {
	document.querySelector(".form1").style.display = "none";
	document.querySelector(".but1").style.color= "white";
	document.querySelector(".but1").style.backgroundColor= "#007bff";
	document.querySelector(".form2").style.display = "block";
	document.querySelector(".but2").style.color= "black";
	document.querySelector(".but2").style.backgroundColor= "white";
}

/* Edit entity */
function setValue(id1, id2) {
	document.getElementById(id1).value = document.getElementById(id2).innerText
}

function setTeacher(id) {
	document.getElementById("edit_teacher").value = id
}

function edit(id) {
	setValue("edit_id", "id" + id)
	setValue("edit_name", "name" + id)
	setValue("edit_age", "age" + id)
	if (document.title.includes("teacher"))
	{
		setValue("edit_contact", "contact" + id)
		setValue("edit_salary", "salary" + id)
		setValue("edit_nic", "nic" + id)
	}
	setValue("edit_gender", "gender" + id)
	setValue("edit_course", "course" + id)
	setValue("edit_fee", "fee" + id)
	setValue("edit_guardian", "guardian" + id)
	setValue("edit_contact", "contact" + id)
	setValue("edit_country", "country" + id)
	let t_id = "t_" + id
	t_id = document.getElementById(t_id).value
	setTeacher(t_id)
}
