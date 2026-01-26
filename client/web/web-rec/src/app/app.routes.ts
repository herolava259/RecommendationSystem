import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SignupComponent } from './account/components/signup/signup.component';

export const routes: Routes = [
    {path: "", component: HomeComponent},
    {
        path: "test",
        loadChildren: () =>
            import("./app.routes.try").then(m => m.testRoutes)
    },
    {
        path: "signup",
        component: SignupComponent
    },

    {path: "**", component: HomeComponent, pathMatch: 'full'}
];
