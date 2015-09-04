/**
 * Created by Zartch on 23/06/2015.
 */

$( document ).ready(function() {

     jQuery.each($("select[multiple]"), function () {
      // "Locations" can be any label you want
      SelectFilter.init(this.id, "subscripcions", 0, "/static/");
     });
 });