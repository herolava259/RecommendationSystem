import { HttpParams } from "@angular/common/http";

export interface Pagination{
    page: number;
    size: number;
    sort: string[];
}


export interface Pageable{
    pageNumber: number;
    pageSize: number;
    sort: number;
    offset: number;
    unpaged: boolean;
}


export interface Sort {
    empty: boolean;
    sorted: boolean;
    unsorted: boolean;
}

export interface Page<T> {
    content: T[];
    pageable: Pageable,
    totalPages: number;
    totalElements: number;
    last?: boolean;
    sort: Sort;
    pageNumber: number;
    pageSize: number;
    first?: boolean;
    numberOfElements: number;
    empty?: boolean;
}

export const createPaginationParams = (req: Pagination): HttpParams => {

    let params = new HttpParams();

    params = params.append("page", req.page).append("size", req.size);

    req.sort.forEach(value => {
        params = params.append("sort", value);
    })

    return params;
}