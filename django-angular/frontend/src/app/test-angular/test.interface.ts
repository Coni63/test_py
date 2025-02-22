// test-data.interface.ts
export interface TestData {
    id: string;
    text: string;
    date: string;
    bool: boolean;
    number: number;
    float: number;
  }
  
  export interface ApiResponse {
    total_records: number;
    matching_records: number;
    start: number;
    size: number;
    current_page: number;
    total_pages: number;
    results: TestData[];
  }
  