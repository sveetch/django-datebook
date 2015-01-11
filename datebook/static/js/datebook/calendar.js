(function( $ ) {

/*
 * Navigation within reveal modal for next/previous day
 */
$.fn.calendar_days_modalnav = function(options) {
    var $container = this,
        options = (options) ? options : {};
        
    $container.on( "click", "a.modal-navigation-day", function(e) {
        var $this = $(this),
            url = $this.attr('href'),
            from_id = $this.attr('data-from-id'),
            target_id = $this.attr('data-target-id');
        
        $.get( url, function(data) {
            $('#revealDayModal > .inner').replaceWith(data);
        //})
        //.fail(function() {
        //    console.log( "error" );
        });
        
        return false;
    });
    
    return this;
};


/*
 * Switch calendar to mosaic/flat view
 */
$.fn.calendar_view_mode = function(options) {
    var $container = this,
        options = (options) ? options : {};
        
    // Switch to calendar mode
    $('.to-mosaic', $container).click(function(e) {
        $('.row.datebook').addClass('large-row-fluid');
        $('.to-flat', $container).addClass('secondary');
        $(this).removeClass('secondary');
        $('.datebook-month').addClass('calendar');
        return false;
    });
    
    // Switch to flat mode
    $('.to-flat', $container).click(function(e) {
        $('.row.datebook').removeClass('large-row-fluid');
        $('.to-mosaic', $container).addClass('secondary');
        $(this).removeClass('secondary');
        $('.datebook-month').removeClass('calendar');
        return false;
    });
    
    return this;
};


/*
 * Daymodels menu selector
 */
$.fn.calendar_daymodel_form = function(options) {
    var $menu = this,
        options = (options) ? options : {},
        defaults = {
            'overlay_selector': ".daymodel-choose-overlay",
            'form_selector': "#daymodel-menu-chooser-form",
            'day_field_selector': "#id_days",
            'daymodel_field_selector': "#id_daymodel"
        };
    
    // Menu buttons actions
    $('.opener', $menu).click(function(e) {
        $(this).hide('fast');
        $('.closer, .form', $menu).show('fast');
        $(defaults.overlay_selector).show('fast');
        return false;
    });
    $('.closer', $menu).click(function(e) {
        $('.opener', $menu).show();
        $('.closer, .form', $menu).hide();
        $(defaults.overlay_selector).hide().removeClass('checked');
        return false;
    });
    
    // Item overlays click event to (un)select day
    $(defaults.overlay_selector).click(function(e) {
        $(this).toggleClass( "checked");
        return false;
    });
    
    // Form submit override to fill the days selection
    $(defaults.form_selector).submit(function( event ) {
        var $form = $(this),
            $submitted_values = [],
            errors = [];
        
        // Resets
        $form.removeClass("has-errors");
        $(defaults.day_field_selector+" option:selected").each(function() {
            $(this).prop("selected", false);
        });
        
        // Cheched overlays select appropriate input's values
        $(defaults.overlay_selector+'.checked').each(function( index ) {
            $submitted_values.push($(this).attr('data-day-date'));
            var day_no = $(this).attr('data-day-date');
            $(defaults.day_field_selector+" option[value='"+day_no+"']", $form).prop("selected", true);
        });
        
        // Validate daymodel selection
        if($(defaults.daymodel_field_selector+" option:selected", $form).length>0){
            if( !$($(defaults.daymodel_field_selector+" option:selected", $form)[0]).val() ) {
                errors.push("You must select a day model.");
            }
        }
        
        // Let the form submit only if there is selected days
        if($submitted_values.length==0){
            errors.push("You must select some days to fill in.");
        }
        
        // Prevent submit if errors
        if(errors.length>0){
            $form.addClass("has-errors");
            event.preventDefault();
            return false;
        }
        
        // // Debug
        // console.log( $( this ).serialize() );
        // event.preventDefault();
        // return false;
        // No errors, let the submit event be triggered
        return true;
    });
    
    return this;
};

}( jQuery ));