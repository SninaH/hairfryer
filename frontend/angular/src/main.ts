import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { FrameworkComponent } from './app/components/framework/framework.component';
bootstrapApplication(FrameworkComponent, appConfig)
  .catch((err) => console.error(err));
