<%inherit file="master.mak"/>
<script type="text/javascript">
  $.extend($.gritter.options, { 
    position: 'bottom-right', // defaults to 'top-right' but can be 'bottom-left', 'bottom-right', 'top-left', 'top-right' (added in 1.7.1)
    fade_in_speed: 'medium', // how fast notifications fade in (string or int)
    fade_out_speed: 500, // how fast the notices fade out
    time: 1500 // hang on the screen for...
  });
</script>
${widget.display() | n}
${moksha_socket.display() |n }
