import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, ViewChild } from '@angular/core';
import { DataTableDirective, DataTablesModule } from "angular-datatables";
import { Config } from 'datatables.net';
import { error } from 'jquery';

interface PokemonResult {
  name: string;
  url: string;
}

interface PokemonResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: PokemonResult[];
}

@Component({
  selector: 'app-test-table',
  standalone: true,
  imports: [DataTablesModule],
  templateUrl: './test-table.component.html',
  styleUrl: './test-table.component.scss'
})
export class TestTableComponent {

  constructor(
    private http: HttpClient
  ) { }

  @ViewChild(DataTableDirective, {static: false})
  datatableElement!: DataTableDirective;

  dtOptions: Config = {};

  ngOnInit(): void {
    const that = this;
    this.dtOptions = {
      serverSide: true,
      lengthChange: false,
      pageLength: 25,
      ajax: (dataTablesParameters: any, callback) => {
        console.log(dataTablesParameters);

        let parsedParams = {
          limit: dataTablesParameters["length"],
          offset: dataTablesParameters["start"],
          order_column: "",
          order_direction: "",
          search: dataTablesParameters["search"]["value"],
        }

        if (dataTablesParameters["order"].length > 0) {
          let idx = dataTablesParameters["order"][0]["column"]
          let dir = dataTablesParameters["order"][0]["dir"]
          parsedParams.order_column = dataTablesParameters["columns"][idx]["data"];
          parsedParams.order_direction = dir
        }



        console.log(parsedParams);

        that.http
          .get<PokemonResponse>(
            'https://pokeapi.co/api/v2/pokemon',
            {
              observe: 'body', // This ensures you are only interested in the response body.
              params: parsedParams // Assuming `dataTablesParameters` is of the type `HttpParams`.
            }
          ).subscribe(response => {
            console.log('Server response:', response);
            callback({
              recordsTotal: response.count,
              recordsFiltered: response.count,
              data: response.results
            });
          });

            
      },
      columns: [{
        title: 'name',
        data: 'name'
      }, {
        title: 'Link',
        data: 'url'
      }]
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
