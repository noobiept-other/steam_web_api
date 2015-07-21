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
var tables = document.getElementsByClassName( 'SortTable' );

if ( tables.length === 0 )
    {
    return;
    }


for (var a = tables.length - 1 ; a >= 0 ; a--)
    {
    var headers = tables[ a ].getElementsByTagName( 'th' );

    for (var b = headers.length - 1 ; b >= 0 ; b--)
        {
        var header = headers[ b ];

        if ( header.classList.contains( 'SortTable-sortable' ) )
            {
            header.addEventListener( 'click', getHeaderClickListener( b ) );
            }
        }
    }
};


/**
 * Returns the click listener that will trigger the sorting of the table.
 */
function getHeaderClickListener( position )
{
var descending = true;

return function( event )
    {
    var th = event.target;
    var tbody = th.parentElement.parentElement.nextElementSibling;
    descending = !descending;

    sortTable( tbody, position, descending );
    };
}


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

        // see if its a number
    var dataNumber = Number( dataValue );

    if ( isNaN( dataNumber ) )
        {
            // its a string, lower the case for the sorting
        dataValue = dataValue.toLowerCase();
        }

    else
        {
        dataValue = dataNumber;
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



var parent = tbody.parentNode;
var next = tbody.nextSibling;

    // remove the 'tbody' element from the tree, before making the changes
parent.removeChild( tbody );

    // re-add the rows to the table
for (a = 0 ; a < data.length ; a++)
    {
    tbody.appendChild( data[ a ].row );
    }

    // re-add the 'tbody' element to the tree
parent.insertBefore( tbody, next );
}


})(SortTable || (SortTable = {}));


window.addEventListener( 'load', SortTable.init );