from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.kaala.helper import response, response_for_created_leave_type, response_for_user_leave_type, \
    response_for_all_leave_types, get_leaves_types_list, response_for_created_leave
from app.models import User, LeaveTypes, Leaves

# Initialize blueprint
leaveType = Blueprint('leaveType', __name__)
leaves = Blueprint('leaves', __name__)

@leaveType.route('/leaveType/', methods=['POST'])
@token_required
def create_leave_type(current_user):
    """
    Create a Leave_Type from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        leaveType_name = data.get('leaveType')
        description = data.get('description')
        num_of_days = data.get('num_of_days')
        validity = data.get('validity')
        carry_forward = data.get('carry_forward')
        employee_id = current_user.id
        if leaveType_name:
            leaveType = LeaveTypes(leaveType_name, description, num_of_days, validity, carry_forward, employee_id)
            leaveType.save()
            return response_for_created_leave_type(leaveType, 201)
        return response('failed', 'Missing leaveType name attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@leaveType.route('/leaveType/<leave_type_id>', methods=['GET'])
@token_required
def get_leave_type(current_user, leave_type_id):
    """
    Return a user Leave_Type with the supplied user Id.
    :param current_user: User
    :param Leave_Type_id: Leave_Type Id
    :return:
    """
    try:
        int(leave_type_id)
    except ValueError:
        return response('failed', 'Please provide a valid Leave_Type Id', 400)
    else:
        leave_type = LeaveTypes.query.filter_by(id=leave_type_id).first()
        if leave_type:
            return response_for_user_leave_type(leave_type)
        return response('failed', "leave_type not found", 404)

@leaveType.route('/leaveType/', methods=['GET'])
@token_required
def get_all_leave_types(current_user):
    """
    Return a user Leave_Type with the supplied user Id.
    :param current_user: User
    :param Leave_Type_id: Leave_Type Id
    :return:
    """
    leaveTypes = LeaveTypes.query.all()

    if leaveTypes:
        return response_for_all_leave_types(get_leaves_types_list(leaveTypes))
    else:
        return response('failed', "LeaveTypes not found", 404)

@leaveType.route('/leaveType/<leave_type_id>', methods=['PUT'])
@token_required
def edit_leave_type(current_user, leave_type_id):

    if request.content_type == 'application/json':
        data = request.get_json()
        leaveType_name = data.get('leaveType')
        description = data.get('description')
        num_of_days = data.get('num_of_days')
        validity = data.get('validity')
        carry_forward = data.get('carry_forward')
        employee_id = current_user.id
        try:
            int(leave_type_id)
        except:
            return response('failed', 'Please provide a valid leave type Id', 400)

        leave_type = LeaveTypes.query.filter_by(id=leave_type_id).first()
        if leave_type:
            leave_type.update(leaveType_name)
            leave_type.update(description)
            leave_type.update(num_of_days)
            leave_type.update(validity)
            leave_type.update(carry_forward)
            leave_type.update(employee_id)
            return response_for_created_leave_type(leave_type, 201)
        return response('failed', 'The leaveType with Id ' + leave_type_id + ' does not exist', 404)
    return response('failed', 'Content-type must be json', 202)


@leaveType.route('/leaveType/<leave_type_id>', methods=['DELETE'])
@token_required
def delete_leave_type(current_user, leave_type_id):

    try:
        int(leave_type_id)
    except:
        return response('failed', 'Please provide a valid leave type Id', 400)

    leave_type = LeaveTypes.query.filter_by(id=leave_type_id).first()

    if not leave_type:
        abort(404)
    leave_type.delete()
    return response('success', 'LeaveType Deleted successfully', 200)



@leaves.route('/leaves/', methods=['POST'])
@token_required
def create_leave(current_user):
    """
    Create a Leave from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        leaveType = data.get('leaveType')
        description = data.get('description')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        num_of_days = data.get('num_of_days')
        employee_id = current_user.id
        status = data.get('status')

        if leaveType:
            leave = Leaves(leaveType, description, from_date, to_date, num_of_days, employee_id, status)
            leave.save()
            return response_for_created_leave(leave, 201)
        return response('failed', 'Missing leaveType attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@leaves.route('/leaves/<leave_id>', methods=['GET'])
@token_required
def get_leave(current_user, leave_id):
    """
    Return a user Leave_Type with the supplied user Id.
    :param current_user: User
    :param Leave_Type_id: Leave_Type Id
    :return:
    """
    try:
        int(leave_id)
    except ValueError:
        return response('failed', 'Please provide a valid Leave_Type Id', 400)
    else:
        leave = Leaves.query.filter_by(id=leave_id).first()
        if leave:
            return response_for_created_leave(leave, 200)
        return response('failed', "leave_type not found", 404)

