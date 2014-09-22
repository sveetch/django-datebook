/*
 * Vacation input
 */
function button_switch(holder, options){
    $('label, input', holder).hide();
    
    holder.append('<a href="#" class="button vacation-switch off" data-switch-value="false" data-switch-to=".vacation-switch.on" style="display:none;">'+options.vacation_off_label+'</a><a href="#" class="button secondary vacation-switch on" data-switch-value="true" data-switch-to=".vacation-switch.off" style="display:none;">'+options.vacation_on_label+'</a>');
    
    function apply_vacation_display(holder){
        holder.parents("form")
            .find(".row.opacited").css('opacity', '0.4')
            .find("input, textarea").prop('readonly',true);
        $('a.vacation-switch.off', holder).show();
    }
    
    function remove_vacation_display(holder){
        holder.parents("form")
            .find(".row.opacited").css('opacity', '1.0')
            .find("input, textarea").prop('readonly',false);
        $('a.vacation-switch.on', holder).show();
    }
    
    // Apply display from initial checkbox value
    if($('input:checked', holder).length){
        apply_vacation_display(holder);
    } else {
        remove_vacation_display(holder);
    }
    
    // Watch for checkbox value changes
    $('a.vacation-switch', holder).click(function(e) {
        var $this = $(this),
            $target = $($this.attr('data-switch-to'), holder)
            $value = $this.attr('data-switch-value')=='true' ? true : false;
            $this.hide();
            $target.show();
            $('input', holder).prop('checked', $value);
            if($value){
                apply_vacation_display(holder);
            } else {
                remove_vacation_display(holder);
            }
        
        return false;
    });
    
}

/*
 * Initialize day form for all its inputs stuff
 */
function init_form(day_form, options){
    options = (options) ? options : {};
    // Init timepicker on time inputs
    $('#id_start_datetime_1, #id_stop_datetime_1', day_form).timepicker({ 'timeFormat': 'H:i' });
    $('#id_pause, #id_overtime', day_form).timepicker({ 'timeFormat': 'H:i' });
    // Hide date inputs to avoid manual edit
    $('#id_start_datetime_0, #id_stop_datetime_0', day_form).hide();
    
    /*
    * Automatically update the stop date on start & stop time inputs changes
    * 
    * If diff between start and stop is less than 0, assume the stop time is in the 
    * next day (from the start date), else assume it is in the same day that the 
    * start date.
    *
    * Ex: If start is "15/05/2013 11:00" and stop time is "02:00", stop date will be 
    *     "16/05/2013". Then if stop time become "18:00", stop date will be "15/05/2013".
    */
    $('#id_start_datetime_1, #id_stop_datetime_1', day_form).on('changeTime', function() {
        var mstart = moment($("#id_start_datetime_0", day_form).val() +" "+ $("#id_start_datetime_1", day_form).val(), "DD/MM/YYYY HH:mm"),
            mstop = moment($("#id_stop_datetime_0", day_form).val() +" "+ $("#id_stop_datetime_1", day_form).val(), "DD/MM/YYYY HH:mm"),
            startdate = moment($("#id_start_datetime_0", day_form).val(), "DD/MM/YYYY");
        
        // Update stop date from diff with start datetime
        if(mstop.diff(mstart, 'minutes') < 0) {
            startdate.add('days', 1);
            $("#id_stop_datetime_0", day_form).val( startdate.format("DD/MM/YYYY") );
        }
        $("#id_stop_datetime_0", day_form).val( startdate.format("DD/MM/YYYY") );
    });

    button_switch($('#div_id_vacation', day_form), options);
}

