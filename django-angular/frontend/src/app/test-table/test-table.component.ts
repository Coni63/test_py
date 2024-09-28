import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, ViewChild } from '@angular/core';
import { DataTableDirective, DataTablesModule } from "angular-datatables";
import { Config } from 'datatables.net';
import { error } from 'jquery';

// https://l-lin.github.io/angular-datatables/#/advanced/individual-column-filtering
// https://datatables.net/

interface User {
  id: number;
  first_name: string;
  last_name: string;
  country: string;
  city: string;
  age: number;
}

interface ApiResponse {
  total: number;
  filtered: number;
  offset: number;
  items: User[];
}

@Component({
  selector: 'app-test-table',
  standalone: true,
  imports: [DataTablesModule],
  templateUrl: './test-table.component.html',
  styleUrl: './test-table.component.scss'
})
export class TestTableComponent {

  constructor(private http: HttpClient) { }

  @ViewChild(DataTableDirective, {static: false})
  datatableElement!: DataTableDirective;

  dtOptions: Config = {};

  ngOnInit(): void {
    const that = this;
    this.dtOptions = {
      serverSide: true,
      lengthChange: false,
      searching: true,
      orderMulti: true,
      processing: true,
      pageLength: 15,
      // dom: 'lrtip',
      layout: {
        topStart: null,
        topEnd: null,
        bottomStart: 'info',
        bottomEnd: 'paging'
      },
      
      ajax: (dataTablesParameters: any, callback) => {
        console.log(dataTablesParameters);

        that.http
          .post<ApiResponse>(
            '/data',
            dataTablesParameters
          ).subscribe(response => {
            console.log('Server response:', response);
            callback({
              recordsTotal: response.total,
              recordsFiltered: response.filtered,
              data: response.items
            });
          });

            
      },
      columns: [
        {
          title: 'id',
          data: 'id'
        }, 
        {
          title: 'first_name',
          data: 'first_name'
        }, 
        {
          title: 'last_name',
          data: 'last_name'
        }, 
        {
          title: 'country',
          data: 'country'
        }, 
        {
          title: 'city',
          data: 'city'
        }, 
        {
          title: 'age',
          data: 'age'
        }, 
    ]
    };
  }
  

  ngAfterViewInit(): void {
    this.datatableElement.dtInstance.then(dtInstance => {
      dtInstance.columns().every(function () {
        const that = this;
        $('input', this.footer()).on('keyup change', function () {
          clearTimeout($.data(this, 'timer'));

          var waitTime = 500;  // 500ms debounce time
          var self = this;
          
          var timer = setTimeout(function () {
            let inputValue = $(self).val()?.toString();
            inputValue = inputValue ? inputValue : "";
            if (that.search() !== inputValue) {
              that
                .search(inputValue)
                .draw();
            }
          }, waitTime);
    
          $.data(this, 'timer', timer);
        });
      });
    });
  }

}
