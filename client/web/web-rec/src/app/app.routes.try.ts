import { Routes } from '@angular/router'
import { SignupComponent } from './account/components/signup/signup.component'
import { AccountInformationStepComponent } from './account/components/signup/account-information-step/account-information-step.component'

export const testRoutes : Routes = [
    {
        path: "signup",
        component: SignupComponent
    },
    {
        path: "signupstepone",
        component: AccountInformationStepComponent
    }
]