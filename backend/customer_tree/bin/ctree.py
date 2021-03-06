from anytree import Node, RenderTree
from anytree import AnyNode
from anytree import search
from globals import g_logger, g_cfg
from sortedcontainers import SortedSet

class CustomerTree():
    def __init__(self, db, rwlock):
        self.root = None
        self.data_source = db
        self.lock = rwlock

    def add_devnum_upwards(self, node):
        while node is not None:
            node.total_dev_num = node.total_dev_num + 1
            node = node.parent

    def rem_devnum_upwards(self, node):
        while node is not None:
            node.total_dev_num = node.total_dev_num - 1
            node = node.parent

    def init_fromdb(self):
        ent_gen = self.data_source.load_all_ent()
        for ent in ent_gen:
            if ent['pid'] == 0:
                # some interface about dev_ids need to be paged, so it has to be ordered
                self.root = AnyNode(login_name=ent['login_name'], id=ent['eid'],phone=ent['phone'],
                                    addr=ent['addr'], email=ent['email'], dev_ids=SortedSet(), total_dev_num=0,
                                    permission=ent['permission'], logo_url=ent['logo_url'], parent=None)
                continue
            myparent = search.find_by_attr(self.root, name='id', value=ent['pid'])
            node = AnyNode(login_name=ent['login_name'], id=ent['eid'],phone=ent['phone'],
                           addr=ent['addr'], email=ent['email'], dev_ids=SortedSet(), total_dev_num=0,
                           permission=ent['permission'], logo_url=ent['logo_url'], parent=myparent)
        device_gen = self.data_source.load_all_device()
        cache_node = {}
        for device in device_gen:
            owner = cache_node.get(device['eid'])
            if owner is None:
                owner = search.find_by_attr(self.root, name='id', value=device['eid'])
                if owner is None:
                    g_logger.info('can not find eid {}'.format(device['eid']))
                    continue
                owner.dev_ids.add(device['dev_id'])
                self.add_devnum_upwards(owner)
                cache_node[device['eid']] = owner
            else:
                owner.dev_ids.add(device['dev_id'])
                self.add_devnum_upwards(owner)
        self.dump_tree()


    def dump_tree(self):
        g_logger.info(RenderTree(self.root))

    def insert_device(self, event):
        with self.lock.gen_wlock():
            owner = search.find_by_attr(self.root, name='id', value=event['eid'])
            if owner is None:
                g_logger.error('eid:{} invalid, event:{}'.format(event['eid'], event))
                return
            owner.dev_ids.add(event['dev_id'])
            self.add_devnum_upwards(owner)

    def insert_ent(self, event):
        with self.lock.gen_wlock():
            parent = search.find_by_attr(self.root, name='id', value=event['pid'])
            if parent is None:
                g_logger.error('pid:{} invalid, event:{}'.format(event['pid'], event))
                return
            node = AnyNode(login_name=event['login_name'], id=event['eid'], phone=event['phone'],
                addr=event['addr'], email=event['email'], dev_ids=set(), total_dev_num=0,
                permission=event['permission'], logo_url=event['logo_url'], parent=parent)

        self.dump_tree()

    def update_device(self, event):
        old_eid = event.get('old_eid', None)
        if old_eid is None:
            g_logger.info('old_eid is none {}'.format(old_eid))
            return
        with self.lock.gen_wlock():
            old_owner = search.find_by_attr(self.root, name='id', value=event['old_eid'])
            if old_owner is None:
                g_logger.error('eid:{} invalid, event:{}'.format(event['eid'], event))
                return
            old_owner.dev_ids.remove(event['dev_id'])
            self.rem_devnum_upwards(old_owner)
            new_owner = search.find_by_attr(self.root, name='id', value=event['eid'])
            if new_owner is None:
                g_logger.error('eid:{} invalid, event:{}'.format(event['eid'], event))
                return
            new_owner.dev_ids.add(event['dev_id'])
            self.add_devnum_upwards(new_owner)


    def update_ent(self, event):
        with self.lock.gen_wlock():
            node = search.find_by_attr(self.root, name='id', value=event['eid'])
            modified_keys = [key for key in event if key.startswith('old_')]
            orig_keys = [key[4:] for key in modified_keys]
            for key in modified_keys:
                if key.lower() == 'old_pid':
                    orig_key = key[4:]
                    newparent = search.find_by_attr(self.root, name='id', value=event[orig_key])
                    node.parent = newparent
                if key.lower() == 'old_addr':
                    orig_key = key[4:]
                    node.addr = event[orig_key]
                if key.lower() == 'old_phone':
                    orig_key = key[4:]
                    node.phone = event[orig_key]
                if key.lower() == 'old_email':
                    orig_key = key[4:]
                    node.email = event[orig_key]
                if key.lower() == 'old_permission':
                    orig_key = key[4:]
                    node.permission = event[orig_key]
                if key.lower() == 'old_logo_url':
                    orig_key = key[4:]
                    node.logo_url = event[orig_key]
        self.dump_tree()


    def delete_device(self, event):
        with self.lock.gen_wlock():
            owner = search.find_by_attr(self.root, name='id', value=event['eid'])
            if owner is None:
                g_logger.error('eid:{} invalid, event:{}'.format(event['eid'], event))
                return
            owner.dev_ids.remove(event['dev_id'])
            self.rem_devnum_upwards(owner)


    def delete_ent(self, event):
        with self.lock.gen_wlock():
            node = search.find_by_attr(self.root, name='id', value=event['eid'])
            if node is None:
                g_logger.error('eid:{} invalid, event:{}'.format(event['eid'], event))
                return
            node.parent = None

        self.dump_tree()



