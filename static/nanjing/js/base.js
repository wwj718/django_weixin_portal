 /*溢出文字删除*/
$.fn.fonts = function(option){
    option = $.extend({},$.fn.fonts.option,option);
    return this.each(function(){
    var objString = $(this).text(),
        objLength = $(this).text().length,
      num = option.fontNum;
    if(objLength > num){
            objString = $(this).text(objString.substring(0,num) + "...");
    }
                  })
  }
  // default options
      $(".articles_list_dscrip").fonts({
        fontNum:35 
            });
 $(".articles_list_title").fonts({
        fontNum:12
            });

   /*End溢出文字删除*/