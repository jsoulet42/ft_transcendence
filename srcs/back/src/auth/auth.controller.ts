import { Controller, Post }  from '@nestjs/common';
import { AuthService } from './auth.services';

@Controller('auth')
export class AuthController{
	constructor(private authService: AuthService){}

	@Post('signup')
	signup() {
		return 'je signup';
	}

	@Post('signin')
	signin() {
		return 'je signin';
	}
}