$(function(){
    //===== Datatables =====//
    //
    //    //oTable = $('#data-table').dataTable({
    //            //"bJQueryUI": false,
    //                    //"bAutoWidth": false,
    //                            //"sPaginationType": "full_numbers",
    //                                    //"sDom": '<"datatable-header"fl>t<"datatable-footer"ip>',
    //                                           //"sEmptyTable":"表中无数据存在！",
    //                                                   //"oLanguage": {
    //                                                               //"sSearch": "<span>搜索:</span> _INPUT_",
    //                                                                           //"sLengthMenu": "<span>展示条数:</span> _MENU_",
    //                                                                                       //"oPaginate": { "sFirst": "第一页", "sLast": "最后一页", "sNext": ">", "sPrevious": "<" }
    //                                                                                               //}
    //                                                                                                   //});
    //
    //
    //                                                                                                       oTable = $(".media-table").dataTable({
    //                                                                                                               "bJQueryUI": false,
    //                                                                                                                       "bAutoWidth": false,
    //                                                                                                                               "sPaginationType": "full_numbers",
    //                                                                                                                                       "sDom": '<"datatable-header"fl>t<"datatable-footer"ip>',
    //                                                                                                                                               "oLanguage": {
    //                                                                                                                                                       "sSearch": " _INPUT_ <input type='button' value='搜索' id='search' class='btn' style='margin:0;vertical-align:middle;'/>",
    //                                                                                                                                                              "sEmptyTable":"表中无数据存在！",
    //                                                                                                                                                                          "sLengthMenu": "<span>展示条数:</span> _MENU_",
    //                                                                                                                                                                                      "oPaginate": { "sFirst": "第一页", "sLast": "最后一页", "sNext": ">", "sPrevious": "<" }
    //                                                                                                                                                                                              },
    //                                                                                                                                                                                                      "aoColumnDefs": [
    //                                                                                                                                                                                                                { "bSortable": false, "aTargets": [ 0, 4 ] }
    //                                                                                                                                                                                                                        ]
    //                                                                                                                                                                                                                            });
    //                                                                                                                                                                                                                                $('.dataTables_filter input').unbind('keyup')
    //                                                                                                                                                                                                                                    $('#search').click(function(){
    //                                                                                                                                                                                                                                            oTable.fnFilter($(this).siblings('input[type=text]').val())
    //                                                                                                                                                                                                                                                })
    //                                                                                                                                                                                                                                                    $('.pull-right').prependTo($('.datatable-header'))
    //
    //                                                                                                                                                                                                                                                        $('.dropdown').click(function(){
    //                                                                                                                                                                                                                                                                var $that = $(this)
    //                                                                                                                                                                                                                                                                        if($that.hasClass('open')){
    //                                                                                                                                                                                                                                                                                    return $(this).removeClass('open')
    //                                                                                                                                                                                                                                                                                            }
    //                                                                                                                                                                                                                                                                                                    $(this).addClass('open')
    //                                                                                                                                                                                                                                                                                                        })
    //
    //                                                                                                                                                                                                                                                                                                        })
