from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cb7d03fc878'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visit',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('proposed_time', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['property.id'], name='fk_visit_property'),  # Asignar nombre a la clave foránea
        sa.ForeignKeyConstraint(['tenant_id'], ['user.id'], name='fk_visit_tenant'),  # Asignar nombre a la clave foránea
        sa.PrimaryKeyConstraint('id')
    )

    # Modificar tabla 'photo'
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('url',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('property_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # Modificar tabla 'property'
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('type',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(),
               existing_nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # Modificar tabla 'user'
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('username',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.TEXT(),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               nullable=True)
        batch_op.create_unique_constraint('uq_user_username', ['username'])  # Asignar nombre a la restricción UNIQUE
        batch_op.create_unique_constraint('uq_user_email', ['email'])  # Asignar nombre a la restricción UNIQUE

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')  # Eliminar la restricción UNIQUE por nombre
        batch_op.drop_constraint('uq_user_email', type_='unique')  # Eliminar la restricción UNIQUE por nombre
        batch_op.alter_column('role',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=200),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.Float(),
               type_=sa.REAL(),
               existing_nullable=False)
        batch_op.alter_column('type',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.alter_column('property_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('url',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    op.drop_table('visit')
    # ### end Alembic commands ###
