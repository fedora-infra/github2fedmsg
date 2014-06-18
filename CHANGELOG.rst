Changelog
=========

0.3.1
-----

- Adapt this to handle webhook payloads as well as pubsubhubbub. `b821dbf99 <https://github.com/fedora-infra/github2fedmsg/commit/b821dbf99bda1e1ed3897db00336274c36f05c93>`_

0.3.0
-----

- Fix refresh link redirection for @pypingou. `f9d0aad9e <https://github.com/fedora-infra/github2fedmsg/commit/f9d0aad9e976618e7dff452d415a9af1d1aa3f6c>`_
- Remove some debugging. `5cd637945 <https://github.com/fedora-infra/github2fedmsg/commit/5cd637945c63e093428b974ef6ce06ec8004fbfa>`_
- Construct a nice url when new repos are added. `8b22a8931 <https://github.com/fedora-infra/github2fedmsg/commit/8b22a89318f368aebb17c002bead96056b83c6e0>`_
- Remove unused utilities. `a98642c10 <https://github.com/fedora-infra/github2fedmsg/commit/a98642c10564af330922a4a1cf1ae555d07f7c9e>`_
- Reduce oauth scope. `f093b633b <https://github.com/fedora-infra/github2fedmsg/commit/f093b633b7384719e2bbbc4ae37bae651da5838c>`_
- Modern requests works fine here. `9ceb3110b <https://github.com/fedora-infra/github2fedmsg/commit/9ceb3110b893f2e57d01a593883bf019d1754718>`_
- That reduced oauth scope doesn't actually work. `b9cc0892d <https://github.com/fedora-infra/github2fedmsg/commit/b9cc0892d0b6c2a161ca518f2846858613c44b78>`_
- Update consumer key. `1789b722f <https://github.com/fedora-infra/github2fedmsg/commit/1789b722f11a7416bc06ee88d4fa6f1dd160d268>`_
- Break toggling out into its own util function. `ad60e5c23 <https://github.com/fedora-infra/github2fedmsg/commit/ad60e5c231c74ee8aff6f70328952823948f0510>`_
- Port from pubsubhubbub to webhooks. `08cc079cd <https://github.com/fedora-infra/github2fedmsg/commit/08cc079cda5551136c245ac17459930220063b9d>`_
- These scopes work now.  /cc @puiterwijk `fad7394e7 <https://github.com/fedora-infra/github2fedmsg/commit/fad7394e70583497cb3ca02676fb60ea7dc79429>`_
- Just reorganize some of these views.. `1641c5b82 <https://github.com/fedora-infra/github2fedmsg/commit/1641c5b827af6022286afc309370a565cb51b988>`_

0.2.7
-----

- Get relative urls right for serving behind a proxy. `6d60f5170 <https://github.com/fedora-infra/github2fedmsg/commit/6d60f5170c2e2a6d3d852412a2e1743fa1405b8c>`_
- Add new vars to development.ini `935292e2d <https://github.com/fedora-infra/github2fedmsg/commit/935292e2d3a3113d8646afa15c4bef2dcb369f5a>`_

0.2.6
-----

- Remove currently unused alembic stuff. `655844396 <https://github.com/fedora-infra/github2fedmsg/commit/6558443960bf4a2e8f656d0821729d5712a7d1e6>`_

0.2.5
-----

- Include templates and alembic stuff. `92147d6dc <https://github.com/fedora-infra/github2fedmsg/commit/92147d6dc4f057ceedc7e021f0b265d091ae3939>`_

0.2.4
-----

- Update to the lastest bootstrap-fedora. `62cc2def2 <https://github.com/fedora-infra/github2fedmsg/commit/62cc2def29e92abebd37b7bfaf3dc09691e24057>`_

0.2.3
-----

- Add jquery back in. `8985732f1 <https://github.com/fedora-infra/github2fedmsg/commit/8985732f1e22a565dfd3ce9964896e9e4f86657e>`_
- This is gone. `b0e2e309f <https://github.com/fedora-infra/github2fedmsg/commit/b0e2e309f7eb9d00250e9cb164c3a4a3da141877>`_
- Add agpl header notice to each .py file. `52063ac07 <https://github.com/fedora-infra/github2fedmsg/commit/52063ac07ad83a1ddceeb1c12a9ec93ebc6c65f1>`_
- Grammar/style fixes in the README. `ba1a8ead4 <https://github.com/fedora-infra/github2fedmsg/commit/ba1a8ead4736a2e9607a886a0a973721b1017387>`_
- Merge pull request #7 from fedora-infra/feature/review-items `f891d6c4a <https://github.com/fedora-infra/github2fedmsg/commit/f891d6c4a851c2ea381307b1811a3d2d7e21362e>`_

0.2.2
-----

- Include license fulltext. `29e06e62d <https://github.com/fedora-infra/github2fedmsg/commit/29e06e62de6d92ff8e6eb5eafccf5548113282da>`_
- Include tw2.core. `b9483c25e <https://github.com/fedora-infra/github2fedmsg/commit/b9483c25e845cd0656a59cfa8409f6f5fb360304>`_
- We don't really require these things. `5259948c3 <https://github.com/fedora-infra/github2fedmsg/commit/5259948c36b1ca43008734c1f486f55c3d42af05>`_

0.2.1
-----

- Fix inclusion of resources in the dist. `e43d151d5 <https://github.com/fedora-infra/github2fedmsg/commit/e43d151d51620240e1f16befaa999314f31e1da3>`_

0.2
---

- Prune secret.ini. `ec496f86b <https://github.com/fedora-infra/github2fedmsg/commit/ec496f86b6415c6cb988b7c62baa3868efd8908a>`_
