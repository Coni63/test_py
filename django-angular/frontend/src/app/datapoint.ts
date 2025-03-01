export interface Datapoint {
    id: string,
    initialValue: string,
    validatedValue: string | null,
    key: string,
    isValidated: boolean,
    page: number | null
  }