var SortTable;
(function(SortTable) {


/**
 * Initialize the table.
 * Set the click listeners in the table header, to sort the table by that property.
 *
 * - The <table> elements need to have the css class `SortTable`.
 * - The <th> (table header) elements of the columns that are sortable, need to have the class `SortTable-sortable`.
 * - The <td> (table data) elements of the sortable columns, need to have a `data-value` attribute.
 */
SortTable.init = function()
{
var table = document.querySelector( '.SortTable' );

if ( !table )
    {
    return;
    }

var headers = table.querySelectorAll( 'th' );

var click_f = function( position )
    {
    var descending = true;

    return function( event )
        {
        var th = event.target;
        var tbody = th.parentElement.parentElement.nextElementSibling;
        descending = !descending;

        sortTable( tbody, position, descending );
        };
    };

for (var a = headers.length - 1 ; a >= 0 ; a--)
    {
    var header = headers[ a ];

    if ( header.classList.contains( 'SortTable-sortable' ) )
        {
        header.addEventListener( 'click', click_f( a ) );
        }
    }
};


/**
 * Sort the table, based on a column's values.
 */
function sortTable( tbody, position, descending )
{
var rows = tbody.children;
var data = [];
var a;

    // get all the data and reference to the rows
for (a = 0 ; a < rows.length ; a++)
    {
    var row = rows[ a ];
    var dataValue = row.children[ position ].getAttribute( 'data-value' );

    if ( typeof dataValue === 'string' )
        {
        dataValue.toLowerCase();
        }

    data.push({
            row: row,
            data: dataValue
        });
    }

    // sort the data
var less = -1;
var high = 1;

if ( descending === true )
    {
    less = 1;
    high = -1;
    }

data.sort( function( a, b )
    {
    var dataA = a.data;
    var dataB = b.data;

    if ( dataA < dataB )
        {
        return less;
        }

    if ( dataA > dataB )
        {
        return high;
        }

    return 0;
    });


    // re-add the rows to the table
for (a = 0 ; a < data.length ; a++)
    {
    tbody.appendChild( data[ a ].row );
    }
}


})(SortTable || (SortTable = {}));


window.addEventListener( 'load', SortTable.init );