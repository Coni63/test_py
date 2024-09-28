import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, ViewChild } from '@angular/core';
import { DataTableDirective, DataTablesModule } from "angular-datatables";
import { Config } from 'datatables.net';
import { error } from 'jquery';

interface User {
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
      lengthChange: true,
      pageLength: 15,
      ajax: (dataTablesParameters: any, callback) => {
        console.log(dataTablesParameters);

        let parsedParams = {
          limit: dataTablesParameters["length"],
          offset: dataTablesParameters["start"],
          // order_column: "",
          // order_direction: "",
          // search: dataTablesParameters["search"]["value"],
        }

        // if (dataTablesParameters["order"].length > 0) {
        //   let idx = dataTablesParameters["order"][0]["column"]
        //   let dir = dataTablesParameters["order"][0]["dir"]
        //   parsedParams.order_column = dataTablesParameters["columns"][idx]["data"];
        //   parsedParams.order_direction = dir
        // }



        console.log(parsedParams);

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
  

  // ngAfterViewInit(): void {
  //   this.datatableElement.dtInstance.then(dtInstance => {
  //     dtInstance.columns().every(function () {
  //       const that = this;
  //       $('input', this.footer()).on('keyup change', function () {
  //         if (that.search() !== this['value']) {
  //           that
  //             .search(this['value'])
  //             .draw();
  //         }
  //       });
  //     });
  //   });
  // }

}
