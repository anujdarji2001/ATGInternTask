$(document).ready(function() {
    var max = 80;
    $(".blog-card-description").each(function() {
        var str = $(this).text();
        if ($.trim(str).length > max) {
            var subStr = str.substring(0, max);
            var hiddenStr = str.substring(max, $.trim(str).length);
            console.log(hiddenStr)
            $(this).empty().html(subStr);
            $(this).append('<a href="javascript:void(0);" class="link"> Read more…</a>');
            $(this).append('<span class="addText">'+hiddenStr+'</span>');
        }
    });
    $(".link").click(function() {
        $(this).siblings(".addText").contents().unwrap();
        $(this).remove();
    });
  });

const filterContainer=document.querySelector(".portfolio-filter"),
      filterBtns=filterContainer.children,
      totalFilterBtn=filterBtns.length,
      portfolioItems=document.querySelectorAll(".blogmain"),
      totalPortfolioItem= portfolioItems.length;
    
      console.log(totalPortfolioItem)

      for(let i=0;i<totalFilterBtn;i++)
      {
      	filterBtns[i].addEventListener("click",function(){
      		        filterContainer.querySelector(".active").classList.remove("active");
                   this.classList.add("active");


         const filterValue=this.getAttribute("data-filter");
        
         console.log(filterValue)
         for(let k=0;k<totalPortfolioItem;k++){
         	if(filterValue===portfolioItems[k].getAttribute("data-category")){
                portfolioItems[k].classList.remove("hide");
         		portfolioItems[k].classList.add("show");
         	}
         	else{
         		portfolioItems[k].classList.remove("show");
         		portfolioItems[k].classList.add("hide");
         	}

         	if(filterValue==="all"){
                  portfolioItems[k].classList.remove("hide");
         		portfolioItems[k].classList.add("show");

         	}
         }

      	})
      }
