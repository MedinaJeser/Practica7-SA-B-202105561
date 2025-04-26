import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Delete,
    Param,
} from '@nestjs/common';
import { UsersService } from './users.service';
import { User } from './schemas/user.schema';

@Controller('users')
export class UsersController {
    constructor(private readonly usersService: UsersService) { }

    @Get('calificacion')
    async calificacion() {
        return {
        message: 'Calificación obtenida exitosamente',
        status: 'success',
        };
    }

    @Post()
    async create(@Body() userData: Partial<User>): Promise<User> {
        return this.usersService.create(userData);
    }

    @Get()
    async findAll(): Promise<User[]> {
        return this.usersService.findAll();
    }

    @Get(':id')
    async findOne(@Param('id') id: string): Promise<User | null> {
        return this.usersService.findOne(id);
    }

    @Patch(':id')
    async update(
        @Param('id') id: string,
        @Body() userData: Partial<User>,
    ) {
        return this.usersService.update(id, userData);
    }

    @Delete(':id')
    async remove(
        @Param('id') id: string,
    ): Promise<User | null> {
        return this.usersService.remove(id);
    }
}
