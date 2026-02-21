import { Routes } from '@angular/router';
import { Home } from './home/home';
import { About } from './about/about';
import { PaintingsList } from './paintings-list/paintings-list';
import { PaintingDetails } from './painting-details/painting-details';
import { Login } from './login/login';
import { Signup } from './signup/signup';
import { Profile } from './profile/profile';
import { Favorites } from './favorites/favorites';
import { Offline } from './offline/offline';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'about', component: About },
    { path: 'paintings', component: PaintingsList },
    { path: 'paintings/:id', component: PaintingDetails },
    { path: 'login', component: Login },
    { path: 'signup', component: Signup },
    { path: 'favorites', component: Favorites },
    { path: 'offline', component: Offline },
    {
        path: 'profile',
        component: Profile,
        canActivate: [authGuard]
    }
];
